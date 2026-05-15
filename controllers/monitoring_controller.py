from services.alert_service import AlertService

class MonitoringController:

    def __init__(self):
        self.alert = AlertService()

    def detect_drowsiness(self):

        sleepy = True

        if sleepy:
            self.alert.trigger_sound()
            self.alert.trigger_popup()

        return {
            "sleepy_detected": sleepy
        }