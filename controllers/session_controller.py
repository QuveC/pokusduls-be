from models.session import SessionData
from services.gamification_service import GamificationService

class SessionController:

    def __init__(self):
        self.game = GamificationService()

    def complete_session(self, db, data):

        xp = self.game.calculate_xp(
            data.duration,
            0
        )

        session = SessionData(
            user_id=data.user_id,
            method_type=data.method_type,
            duration=data.duration,
            xp_earned=xp
        )

        db.add(session)
        db.commit()
        db.refresh(session)

        return {
            "message": "Session Complete",
            "xp": xp,
            "session_id": session.session_id
        }