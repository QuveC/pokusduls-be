from fastapi import HTTPException
from models.statistics import Statistics


class StatisticsController:

    def get_statistics(self, db, user_id: int):

        stats = db.query(Statistics).filter(
            Statistics.user_id == user_id
        ).first()

        if not stats:
            # Kembalikan nilai default, bukan error — user baru belum punya baris statistik
            return {
                "total_xp": 0,
                "current_streak": 0,
                "total_sessions": 0,
                "total_drowsy_events": 0,
                "avg_focus_score": 0.0,
                "chat_interactions": 0,
            }

        return {
            "total_xp":            stats.total_xp,
            "current_streak":      stats.current_streak,     # nama kolom di DB: current_streak
            "total_sessions":      0,                         # hitung dari session_data jika perlu
            "total_drowsy_events": stats.total_drowsy_events,
            "avg_focus_score":     round(stats.avg_focus_score, 1),
            "chat_interactions":   stats.chat_interactions,
        }
