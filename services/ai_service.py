import os
import re


class AIService:

    def generate_response(self, message: str) -> str:
        """
        Hasilkan respons AI berdasarkan pesan dari user.
        Gunakan Gemini API jika API_KEY tersedia, fallback ke respons lokal.
        """
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if api_key:
            return self._call_gemini(api_key, message)
        return self._local_response(message)

    # ── Gemini API ─────────────────────────────────────────────────────────────
    def _call_gemini(self, api_key: str, message: str) -> str:
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=(
                    "Kamu adalah asisten belajar AI bernama PokusDuls. "
                    "Bantu pengguna dengan tips belajar efektif, teknik Pomodoro, "
                    "Feynman, Active Recall, motivasi, dan manajemen waktu. "
                    "Jawab dalam Bahasa Indonesia yang ramah dan informatif."
                ),
            )
            resp = model.generate_content(message)
            return resp.text
        except Exception as e:
            return self._local_response(message)

    # ── Fallback lokal ─────────────────────────────────────────────────────────
    def _local_response(self, message: str) -> str:
        m = message.lower()

        if any(k in m for k in ["tips", "cara belajar"]):
            return (
                "Berikut tips belajar efektif:\n\n"
                "1. **Pomodoro** - Belajar 25 menit, istirahat 5 menit\n"
                "2. **Active Recall** - Test diri sendiri tanpa melihat catatan\n"
                "3. **Feynman** - Jelaskan konsep dengan bahasa sederhana\n"
                "4. **Spaced Repetition** - Review materi secara berkala\n"
                "5. **Eliminate Distractions** - Fokus penuh saat belajar\n\n"
                "Mau tau lebih detail salah satunya?"
            )
        if "pomodoro" in m:
            return (
                "Teknik Pomodoro adalah metode manajemen waktu:\n\n"
                "1. Pilih tugas\n2. Set timer 25 menit\n3. Kerjakan fokus penuh\n"
                "4. Istirahat 5 menit\n5. Ulangi 4x, lalu istirahat panjang\n\n"
                "Gunakan fitur timer di PokusDuls!"
            )
        if "feynman" in m:
            return (
                "Teknik Feynman: belajar dengan mengajar!\n\n"
                "1. Pilih konsep\n2. Jelaskan seolah ke anak kecil\n"
                "3. Identifikasi bagian yang sulit dijelaskan\n4. Review dan sederhanakan"
            )
        if "active recall" in m:
            return (
                "Active Recall = mengingat tanpa melihat sumber.\n\n"
                "1. Baca materi\n2. Tutup buku\n3. Tulis semua yang diingat\n"
                "4. Cek dan pelajari yang kurang\n5. Ulangi!"
            )
        if any(k in m for k in ["motivasi", "semangat", "capek"]):
            return (
                "💪 Ingat tujuan besarmu! Setiap sesi belajar kecil membawa kamu lebih dekat ke impianmu.\n\n"
                "\"Success is the sum of small efforts repeated day in and day out.\""
            )
        if any(k in m for k in ["fokus", "distraksi", "konsentrasi"]):
            return (
                "Tips Fokus:\n\n"
                "1. Cari tempat tenang\n2. Matikan notifikasi\n"
                "3. Satu tugas dalam satu waktu\n4. Gunakan white noise\n5. Istirahat teratur"
            )

        return (
            "Saya siap membantu! Tanya tentang:\n"
            "• Tips belajar (Pomodoro, Feynman, Active Recall)\n"
            "• Motivasi dan fokus\n"
            "• Time management"
        )
