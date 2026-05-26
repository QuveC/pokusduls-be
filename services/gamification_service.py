from datetime import date


class GamificationService:
    """Diagram: GamificationEngine — calculateXP, updateStreak, calculateFocusBonus, penalizeDrowsiness"""

    def calculate_xp(self, duration: int, drowsy_count: int) -> int:
        base_xp = duration * 10
        penalty = self.penalize_drowsiness(drowsy_count)
        bonus   = self.calculate_focus_bonus(duration, drowsy_count)
        return max(0, base_xp - penalty + bonus)

    def update_streak(self, current_streak: int, last_active: date | None) -> int:
        """Diagram: updateStreak() — increment or reset streak based on last active date."""
        today = date.today()
        if last_active is None:
            return 1
        if last_active == today:
            return current_streak          # already updated today
        if (today - last_active).days == 1:
            return current_streak + 1      # consecutive day
        return 1                           # streak broken

    def calculate_focus_bonus(self, duration: int, drowsy_count: int) -> int:
        """Diagram: calculateFocusBonus() — bonus XP jika tidak ngantuk."""
        if drowsy_count == 0 and duration >= 25:
            return duration * 2
        return 0

    def penalize_drowsiness(self, drowsy_count: int) -> int:
        """Diagram: penalizeDrowsiness() — XP penalty per drowsy event."""
        return drowsy_count * 5
