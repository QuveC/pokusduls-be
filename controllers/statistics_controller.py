from models.statistics import Statistics


class StatisticsController:

    def get_statistics(self, db, user_id):

        stats = db.query(Statistics).filter(
            Statistics.user_id == user_id
        ).first()

        if not stats:
            return {
                "message": "No statistics found"
            }

        return {
            "total_xp": stats.total_xp,
            "streak": stats.streak,
            "total_sessions": stats.total_sessions
        }