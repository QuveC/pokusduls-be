class GamificationService:

    def calculate_xp(self, duration, drowsy_count):
        xp = duration * 10

        penalty = drowsy_count * 5

        return max(0, xp - penalty)

    def update_streak(self, current_streak):
        return current_streak + 1