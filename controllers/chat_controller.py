from services.ai_service import AIService
from models.chat import ChatMessage
from models.statistics import Statistics


class ChatController:
    """Diagram: ChatbotController — sendMessage, pauseTimer, receiveResponse, clearHistory"""

    def __init__(self):
        self.ai = AIService()

    def send_message(self, db, data):
        """Diagram: sendMessage() + receiveResponse()"""
        response = self.ai.generate_response(data.message)

        user_message = ChatMessage(user_id=data.user_id, role="user",    message=data.message)
        ai_message   = ChatMessage(user_id=data.user_id, role="assistant", message=response)
        db.add(user_message)
        db.add(ai_message)

        # Diagram: chatInteractions di UserStatistics
        stats = db.query(Statistics).filter(Statistics.user_id == data.user_id).first()
        if stats:
            stats.chat_interactions = (stats.chat_interactions or 0) + 1

        db.commit()

        return {"response": response}

    def get_history(self, db, user_id: int):
        """Diagram: ChatHistory.getHistory()"""
        messages = (
            db.query(ChatMessage)
            .filter(ChatMessage.user_id == user_id)
            .order_by(ChatMessage.created_at.asc())
            .all()
        )
        return {"history": [m.toJSON() for m in messages]}

    def clear_history(self, db, user_id: int):
        """Diagram: ChatHistory.clearHistory() + ChatbotController.clearHistory()"""
        db.query(ChatMessage).filter(ChatMessage.user_id == user_id).delete()
        db.commit()
        return {"message": "Riwayat chat dihapus"}
