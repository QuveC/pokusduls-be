from fastapi import APIRouter
<<<<<<< HEAD
from controllers.monitoring_controller import MonitoringController
=======
from controllers.monitoring_controller import MonitoringController, FrameInput
>>>>>>> 1925e27 (Penambahan YOLO)

router = APIRouter()

controller = MonitoringController()


@router.get("/monitoring/detect")
def detect_drowsiness():
<<<<<<< HEAD
    return controller.detect_drowsiness()
=======
    return controller.detect_drowsiness()


@router.post("/monitoring/detect-frame")
def detect_frame(body: FrameInput):
    """
    Terima frame kamera dari browser (base64),
    jalankan YOLO + MediaPipe, kembalikan status deteksi.
    """
    return controller.detect_frame(body)


@router.get("/monitoring/debug/classes")
def get_model_classes():
    """
    [DEBUG] Lihat semua class yang dikenali model YOLO.
    Buka di browser: http://localhost:8000/monitoring/debug/classes
    """
    return controller.yolo.get_model_classes()
>>>>>>> 1925e27 (Penambahan YOLO)
