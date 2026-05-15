from fastapi import APIRouter
from controllers.monitoring_controller import MonitoringController

router = APIRouter()

controller = MonitoringController()


@router.get("/monitoring/detect")
def detect_drowsiness():
    return controller.detect_drowsiness()