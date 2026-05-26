from models.chat import ChatHistory, ChatMessage
from models.statistics import Statistics
from services.ai_service import AIService
import random


class ChatController:

    def __init__(self):
        self.ai = AIService()

    def send_message(self, db, data):
        response = self.ai.generate_response(data.message)

        # Cari atau buat chat_history untuk user ini
        chat_history = db.query(ChatHistory).filter(
            ChatHistory.user_id == data.user_id
        ).order_by(ChatHistory.chat_history_id.desc()).first()

        if not chat_history:
            chat_history = ChatHistory(
                user_id=data.user_id,
                session_id=f"CHAT-{random.randint(1000, 9999)}"
            )
            db.add(chat_history)
            db.flush()

        # Simpan pesan user dan AI
        user_msg = ChatMessage(
            chat_history_id=chat_history.chat_history_id,
            role="user",
            content=data.message
        )
        ai_msg = ChatMessage(
            chat_history_id=chat_history.chat_history_id,
            role="assistant",
            content=response
        )
        db.add(user_msg)
        db.add(ai_msg)

        # Increment chat_interactions di statistik
        stats = db.query(Statistics).filter(
            Statistics.user_id == data.user_id
        ).first()
        if stats:
            stats.chat_interactions = (stats.chat_interactions or 0) + 1

        db.commit()

        return {"response": response}

    def get_history(self, db, user_id: int):
        chat_history = db.query(ChatHistory).filter(
            ChatHistory.user_id == user_id
        ).order_by(ChatHistory.chat_history_id.desc()).first()

        if not chat_history:
            return {"history": []}

        messages = (
            db.query(ChatMessage)
            .filter(ChatMessage.chat_history_id == chat_history.chat_history_id)
            .order_by(ChatMessage.timestamp.asc())
            .all()
        )
        return {"history": [m.toJSON() for m in messages]}

    def clear_history(self, db, user_id: int):
        chat_history = db.query(ChatHistory).filter(
            ChatHistory.user_id == user_id
        ).all()

        for ch in chat_history:
            db.query(ChatMessage).filter(
                ChatMessage.chat_history_id == ch.chat_history_id
            ).delete()

        db.commit()
        return {"message": "Riwayat chat dihapus"}