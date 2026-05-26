from models.session import SessionData
from models.statistics import Statistics
from services.gamification_service import GamificationService
from datetime import date


class SessionController:

    def __init__(self):
        self.game = GamificationService()

    def complete_session(self, db, data):
        drowsy_count = getattr(data, 'drowsy_count', 0)

        xp = self.game.calculate_xp(data.duration, drowsy_count)

        session = SessionData(
            user_id=data.user_id,
            method_type=data.method_type,
            duration=data.duration,
            drowsy_count=drowsy_count,
            monitoring_enabled=getattr(data, 'monitoring_enabled', False),
            chat_session_id=getattr(data, 'chat_session_id', None),
        )
        db.add(session)

        # Update user_statistics
        stats = db.query(Statistics).filter(
            Statistics.user_id == data.user_id
        ).first()
        today = date.today()

        if not stats:
            stats = Statistics(
                user_id=data.user_id,
                total_xp=0,
                current_streak=0,
                total_drowsy_events=0,
                avg_focus_score=0.0,
                chat_interactions=0,
            )
            db.add(stats)
            db.flush()

        stats.total_xp           = (stats.total_xp or 0) + xp
        stats.total_drowsy_events = (stats.total_drowsy_events or 0) + drowsy_count

        db.commit()
        db.refresh(session)

        return {
            "message":    "Session Complete",
            "xp":         xp,
            "session_id": session.session_id,
        }