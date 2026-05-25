import base64
import os
import numpy as np
import cv2
import mediapipe as mp
from ultralytics import YOLO

# =====================================
# KONFIGURASI MODEL
# Ganti ke "yolov8s.pt" atau "yolov8m.pt" untuk akurasi lebih tinggi
# (akan otomatis diunduh jika belum ada)
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

# Label HP di COCO — class 67 = "cell phone", class 65 = "remote" (mirip bentuknya)
PHONE_LABELS = {"cell phone", "remote"}

# Confidence threshold — turunkan jika sering miss, naikkan jika banyak false positive
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

        # Load MediaPipe FaceMesh
        mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5
        )

    # =====================================
    # HITUNG YAW (sudut kepala kiri/kanan)
    # =====================================
    def _get_yaw(self, landmarks, img_w, img_h):
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
            # Upscale sisi terpanjang ke 640px agar YOLO lebih akurat
            h, w = frame.shape[:2]
            scale = 640 / max(h, w)
            if scale < 1.0:   # hanya upscale, jangan downscale
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

            # Debug: cetak semua objek terdeteksi di console backend
            detected_labels = []
            for r in results:
                for box in r.boxes:
                    cls   = int(box.cls[0])
                    label = self.yolo_model.names[cls]
                    conf  = float(box.conf[0])
                    detected_labels.append(f"{label}({conf:.2f})")
                    # Deteksi HP: "cell phone" ATAU "remote" (mirip bentuknya di kamera)
                    if label in PHONE_LABELS and conf > phone_confidence:
                        phone_detected    = True
                        phone_confidence  = conf
                        matched_label     = label

            if detected_labels:
                print(f"[YOLO] Terdeteksi: {', '.join(detected_labels)}")
            else:
                print("[YOLO] Tidak ada objek terdeteksi")

            # ======= MediaPipe: Deteksi Wajah & Yaw =======
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results_face = self.face_mesh.process(rgb)

            yaw = 0.0
            face_detected = False

            if results_face and results_face.multi_face_landmarks:
                face_detected = True
                for face_landmarks in results_face.multi_face_landmarks:
                    yaw = self._get_yaw(face_landmarks.landmark, img_w, img_h)

            # ======= Logika Distraksi =======
            if phone_detected:
                status = "DISTRACTION: PHONE"
                distraction_type = "phone"
            elif not face_detected:
                status = "DISTRACTION: NO FACE"
                distraction_type = "no_face"
            elif abs(yaw) > 13:
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
            traceback.print_exc()   # cetak full error di console backend
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
        """Kembalikan semua nama class yang dikenali model — untuk debug."""
        return {str(k): v for k, v in self.yolo_model.names.items()}
