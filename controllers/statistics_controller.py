from fastapi import HTTPException
from datetime import date
from models.statistics import Statistics


class StatisticsController:

    def get_statistics(self, db, user_id: int):
        stats = db.query(Statistics).filter(
            Statistics.user_id == user_id
        ).first()

        if not stats:
            return {
                "total_xp":            0,
                "current_streak":      0,
                "total_sessions":      0,
                "total_drowsy_events": 0,
                "avg_focus_score":     0.0,
                "chat_interactions":   0,
            }

        return {
            "total_xp":            stats.total_xp,
            "current_streak":      stats.current_streak,
            "total_sessions":      getattr(stats, 'total_sessions', 0),
            "total_drowsy_events": stats.total_drowsy_events,
            "avg_focus_score":     round(float(stats.avg_focus_score or 0), 1),
            "chat_interactions":   stats.chat_interactions,
        }

    def update_statistics(self, db, user_id: int, xp_gained: int, session_completed: bool):
        """Dipanggil setiap sesi timer selesai — tambah XP + update streak."""
        stats = db.query(Statistics).filter(
            Statistics.user_id == user_id
        ).first()

        today = date.today()

        if not stats:
            # Buat baris baru jika user belum punya statistik
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

        # Tambah XP
        stats.total_xp = (stats.total_xp or 0) + xp_gained

        # Update streak harian
        last_active = getattr(stats, 'last_active_date', None)
        if last_active is None:
            stats.current_streak = 1
        elif last_active == today:
            pass  # sudah belajar hari ini
        elif (today - last_active).days == 1:
            stats.current_streak = (stats.current_streak or 0) + 1
        else:
            stats.current_streak = 1  # streak putus, reset

        if hasattr(stats, 'last_active_date'):
            stats.last_active_date = today

        db.commit()
        db.refresh(stats)

        return {
            "message":        "Statistik diperbarui",
            "total_xp":       stats.total_xp,
            "current_streak": stats.current_streak,
        }
