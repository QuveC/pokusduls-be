from datetime import date


class GamificationService:

    def calculate_xp(self, duration: int, drowsy_count: int) -> int:
        base_xp = duration * 10
        penalty = self.penalize_drowsiness(drowsy_count)
        bonus   = self.calculate_focus_bonus(duration, drowsy_count)
        return max(0, base_xp - penalty + bonus)

    def update_streak(self, current_streak: int, last_active) -> int:
        today = date.today()
        if last_active is None:
            return 1
        if last_active == today:
            return current_streak
        if (today - last_active).days == 1:
            return current_streak + 1
        return 1

    def calculate_focus_bonus(self, duration: int, drowsy_count: int) -> int:
        if drowsy_count == 0 and duration >= 25:
            return duration * 2
        return 0

    def penalize_drowsiness(self, drowsy_count: int) -> int:
        return drowsy_count * 5