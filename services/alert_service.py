class AlertService:
    """Diagram: AlertService — alertType, coolDownTime, triggerSound, triggerVibration, showPopup, logEvent"""

    def __init__(self, alert_type: str = "sound", cool_down_time: int = 30):
        self.alert_type     = alert_type       # diagram: alertType
        self.cool_down_time = cool_down_time   # diagram: coolDownTime

    def trigger_sound(self) -> str:
        """Diagram: triggerSound()"""
        return "Sound Alert Triggered"

    def trigger_vibration(self) -> str:
        """Diagram: triggerVibration()"""
        return "Vibration Alert Triggered"

    def show_popup(self) -> str:
        """Diagram: showPopup()"""
        return "Popup Alert Triggered"

    def trigger_popup(self) -> str:
        """Alias untuk kompatibilitas kode lama."""
        return self.show_popup()

    def log_event(self, event: str) -> dict:
        """Diagram: logEvent()"""
        return {"event": event, "alert_type": self.alert_type}
