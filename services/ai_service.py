import os


class AIService:

    def __init__(self):
        self.api_key    = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self.model_name = os.getenv("AI_MODEL_NAME", "gemini-1.5-flash")

    def generate_response(self, message: str) -> str:
        if self.api_key:
            return self._call_gemini(message)
        return self._local_response(message)

    def build_prompt(self, message: str) -> str:
        return f"{self.fetch_context()}\n\nUser: {message}"

    def fetch_context(self) -> str:
        return (
            "Kamu adalah asisten belajar AI bernama PokusDuls. "
            "Bantu pengguna dengan tips belajar efektif, teknik Pomodoro, "
            "Feynman, Active Recall, motivasi, dan manajemen waktu. "
            "Jawab dalam Bahasa Indonesia yang ramah dan informatif."
        )

    def _call_gemini(self, message: str) -> str:
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=self.fetch_context(),
            )
            return model.generate_content(message).text
        except Exception:
            return self._local_response(message)

    def _local_response(self, message: str) -> str:
        m = message.lower()
        if any(k in m for k in ["tips", "cara belajar"]):
            return "Tips belajar efektif:\n1. Pomodoro\n2. Active Recall\n3. Feynman\n4. Spaced Repetition"
        if "pomodoro" in m:
            return "Pomodoro: belajar 25 menit, istirahat 5 menit. Ulangi 4x lalu istirahat panjang!"
        if "feynman" in m:
            return "Feynman: jelaskan konsep seolah ke anak kecil. Bagian yang susah dijelaskan = belum paham."
        if "active recall" in m:
            return "Active Recall: tutup buku, tulis semua yang kamu ingat. Lebih efektif dari baca ulang!"
        if any(k in m for k in ["motivasi", "semangat", "capek"]):
            return "💪 Tetap semangat! 'Success is the sum of small efforts repeated day in and day out.'"
        if any(k in m for k in ["fokus", "distraksi"]):
            return "Tips fokus:\n1. Tempat tenang\n2. Matikan notifikasi\n3. One task at a time\n4. Gunakan timer!"
        return "Saya siap membantu! Tanya tentang teknik belajar, motivasi, atau time management."