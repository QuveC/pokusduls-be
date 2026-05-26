from fastapi import HTTPException
from datetime import date
from models.statistics import Statistics
from models.session import SessionData


class StatisticsController:

    def get_statistics(self, db, user_id: int):
        stats = db.query(Statistics).filter(
            Statistics.user_id == user_id
        ).first()

        total_sessions = db.query(SessionData).filter(
            SessionData.user_id == user_id
        ).count()

        if not stats:
            return {
                "total_xp":            0,
                "current_streak":      0,
                "total_sessions":      total_sessions,
                "total_drowsy_events": 0,
                "avg_focus_score":     0.0,
                "chat_interactions":   0,
            }

        return {
            "total_xp":            stats.total_xp or 0,
            "current_streak":      stats.current_streak or 0,
            "total_sessions":      total_sessions,
            "total_drowsy_events": stats.total_drowsy_events or 0,
            "avg_focus_score":     round(float(stats.avg_focus_score or 0), 1),
            "chat_interactions":   stats.chat_interactions or 0,
        }

    def update_statistics(self, db, user_id: int, xp_gained: int, session_completed: bool):
        stats = db.query(Statistics).filter(
            Statistics.user_id == user_id
        ).first()

        if not stats:
            stats = Statistics(
                user_id=user_id,
                total_xp=0,
                current_streak=0,
                total_drowsy_events=0,
                avg_focus_score=0.0,
                chat_interactions=0,
            )
            db.add(stats)
            db.flush()

        stats.total_xp = (stats.total_xp or 0) + xp_gained

        db.commit()
        db.refresh(stats)

        return {
            "message":        "Statistik diperbarui",
            "total_xp":       stats.total_xp,
            "current_streak": stats.current_streak,
        }