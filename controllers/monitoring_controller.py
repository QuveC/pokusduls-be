from services.alert_service import AlertService
from services.yolo_service import YOLOService
from fastapi import HTTPException
from pydantic import BaseModel


class FrameInput(BaseModel):
    image: str  # base64 encoded image dari browser


class MonitoringController:

    def __init__(self):
        self.alert = AlertService()
        self.yolo = YOLOService()

    # ─── endpoint lama (tetap ada) ───────────────────────────────────
    def detect_drowsiness(self):
        sleepy = True
        if sleepy:
            self.alert.trigger_sound()
            self.alert.trigger_popup()
        return {"sleepy_detected": sleepy}

    # ─── endpoint baru: terima frame dari browser, jalankan YOLO ─────
    def detect_frame(self, body: FrameInput):
        if not body.image:
            raise HTTPException(status_code=400, detail="Field 'image' wajib diisi")

        result = self.yolo.detect(body.image)
        return result
