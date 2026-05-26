import base64
import os
import numpy as np
import cv2
from ultralytics import YOLO

# =====================================
# LAZY LOADING & MOCK MEDIAPIPE FOR PYTHON 3.13
# =====================================
mp = None
try:
    import mediapipe as _mp
    mp = _mp
except Exception:
    pass

# =====================================
# KONFIGURASI MODEL
# =====================================
MODEL_NAME = os.environ.get("YOLO_MODEL_NAME", "yolov8s.pt")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CANDIDATE_MODEL_PATHS = [
    os.path.join(BASE_DIR, MODEL_NAME),
    os.path.join(BASE_DIR, "..", "model", MODEL_NAME),
    os.path.join(BASE_DIR, "..", "..", "YOLO", MODEL_NAME),
]
if os.environ.get("YOLO_MODEL_PATH"):
    CANDIDATE_MODEL_PATHS.insert(0, os.path.normpath(os.environ["YOLO_MODEL_PATH"]))

MODEL_PATH = None
for path in CANDIDATE_MODEL_PATHS:
    normalized = os.path.normpath(path)
    if os.path.exists(normalized):
        MODEL_PATH = normalized
        break

if MODEL_PATH is None:
    MODEL_PATH = MODEL_NAME  # fallback: biarkan Ultralytics unduh otomatis

# Label HP di COCO — class 67 = "cell phone", class 65 = "remote"
PHONE_LABELS = {"cell phone", "remote"}

# Confidence threshold
CONF_THRESHOLD = float(os.environ.get("YOLO_CONF", "0.10"))

print(f"[YOLO] Model path : {MODEL_PATH}")
print(f"[YOLO] Conf threshold: {CONF_THRESHOLD}")


class YOLOService:
    _instance = None

    def __new__(cls):
        # Singleton agar model hanya dimuat sekali
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

        # Load YOLO model
        self.yolo_model = YOLO(MODEL_PATH)

        # Safe Inisialisasi MediaPipe FaceMesh
        self.face_mesh = None
        global mp
        if mp is not None:
            try:
                # Menggunakan import dinamis saat runtime biar uvicorn lolos startup
                from mediapipe.framework.formats import landmark_pb2
                import mediapipe.python.solutions.face_mesh as mp_fm
                self.face_mesh = mp_fm.FaceMesh(
                    static_image_mode=True,
                    max_num_faces=1,
                    refine_landmarks=True,
                    min_detection_confidence=0.5
                )
                print("[MEDIAPIPE] FaceMesh berhasil di-load via python.solutions.")
            except Exception:
                try:
                    import mediapipe.solutions.face_mesh as mp_fm2
                    self.face_mesh = mp_fm2.FaceMesh(
                        static_image_mode=True,
                        max_num_faces=1,
                        refine_landmarks=True,
                        min_detection_confidence=0.5
                    )
                    print("[MEDIAPIPE] FaceMesh berhasil di-load via direct solutions.")
                except Exception as e:
                    print(f"[WARN] MediaPipe gagal di-load sempurna ({str(e)}). Fallback penuh ke YOLO.")
        else:
            print("[WARN] Module MediaPipe tidak terdeteksi. Fallback penuh ke YOLO.")

    # =====================================
    # HITUNG YAW (sudut kepala kiri/kanan)
    # =====================================
    def _get_yaw(self, landmarks, img_w, img_h):
        try:
            face_2d = []
            face_3d = []
            key_points = [33, 263, 1, 61, 291, 199]

            for idx in key_points:
                x = int(landmarks[idx].x * img_w)
                y = int(landmarks[idx].y * img_h)
                face_2d.append([x, y])
                face_3d.append([x, y, landmarks[idx].z])

            face_2d = np.array(face_2d, dtype=np.float64)
            face_3d = np.array(face_3d, dtype=np.float64)

            focal_length = img_w
            cam_matrix = np.array([
                [focal_length, 0, img_w / 2],
                [0, focal_length, img_h / 2],
                [0, 0, 1]
            ])
            dist_matrix = np.zeros((4, 1))

            success, rot_vec, trans_vec = cv2.solvePnP(
                face_3d, face_2d, cam_matrix, dist_matrix
            )
            if not success:
                return 0.0

            rmat, _ = cv2.Rodrigues(rot_vec)
            angles, _, _, _, _, _ = cv2.RQDecomp3x3(rmat)
            yaw = angles[1] * 360
            return float(yaw)
        except Exception:
            return 0.0

    # =====================================
    # PROSES FRAME UTAMA
    # =====================================
    def detect(self, image_base64: str) -> dict:
        """
        Terima frame sebagai base64 string, proses dengan YOLO + MediaPipe.
        Kembalikan dict berisi status deteksi.
        """
        try:
            # Decode base64 → numpy array
            header, encoded = image_base64.split(",", 1) if "," in image_base64 else ("", image_base64)
            img_bytes = base64.b64decode(encoded)
            np_arr = np.frombuffer(img_bytes, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            if frame is None:
                return {"error": "Gambar tidak valid"}

            img_h, img_w, _ = frame.shape

            # ======= YOLO: Deteksi HP =======
            h, w = frame.shape[:2]
            scale = 640 / max(h, w)
            if scale < 1.0:
                resized = cv2.resize(frame, (int(w * scale), int(h * scale)))
            else:
                resized = cv2.resize(frame, (640, int(h * 640 / w)))

            results = self.yolo_model(
                resized, verbose=False,
                conf=CONF_THRESHOLD,
                iou=0.45
            )
            phone_detected = False
            phone_confidence = 0.0
            matched_label = ""

            detected_labels = []
            for r in results:
                for box in r.boxes:
                    cls   = int(box.cls[0])
                    label = self.yolo_model.names[cls]
                    conf  = float(box.conf[0])
                    detected_labels.append(f"{label}({conf:.2f})")
                    if label in PHONE_LABELS and conf > phone_confidence:
                        phone_detected    = True
                        phone_confidence  = conf
                        matched_label     = label

            if detected_labels:
                print(f"[YOLO] Terdeteksi: {', '.join(detected_labels)}")
            else:
                print("[YOLO] Tidak ada objek terdeteksi")

            # ======= MediaPipe: Deteksi Wajah & Yaw =======
            yaw = 0.0
            face_detected = False

            if self.face_mesh is not None:
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results_face = self.face_mesh.process(rgb)

                if results_face and results_face.multi_face_landmarks:
                    face_detected = True
                    for face_landmarks in results_face.multi_face_landmarks:
                        yaw = self._get_yaw(face_landmarks.landmark, img_w, img_h)

            # ======= Logika Distraksi =======
            if phone_detected:
                status = "DISTRACTION: PHONE"
                distraction_type = "phone"
            elif not face_detected and self.face_mesh is not None:
                status = "DISTRACTION: NO FACE"
                distraction_type = "no_face"
            elif self.face_mesh is not None and abs(yaw) > 13:
                status = "DISTRACTION: LOOKING SIDE"
                distraction_type = "looking_side"
            else:
                status = "FOCUS"
                distraction_type = None

            return {
                "status": status,
                "is_focused": status == "FOCUS",
                "distraction_type": distraction_type,
                "yaw": round(yaw, 2),
                "phone_detected": phone_detected,
                "phone_confidence": round(phone_confidence, 3),
                "matched_label": matched_label,
                "face_detected": face_detected,
                "all_detected": detected_labels,
            }

        except Exception as e:
            import traceback
            traceback.print_exc()
            return {
                "status": "ERROR",
                "is_focused": False,
                "distraction_type": None,
                "yaw": 0.0,
                "phone_detected": False,
                "phone_confidence": 0.0,
                "face_detected": False,
                "all_detected": [],
                "error": str(e)
            }

    def get_model_classes(self) -> dict:
        return {str(k): v for k, v in self.yolo_model.names.items()}