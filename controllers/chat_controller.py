<<<<<<< HEAD
from services.ai_service import AIService
from models.chat import ChatMessage

class ChatController:

    def __init__(self):
        self.ai = AIService()

    def send_message(self, db, data):

        response = self.ai.generate_response(
            data.message
        )

        user_message = ChatMessage(
            user_id=data.user_id,
            role="user",
            message=data.message
        )

        ai_message = ChatMessage(
            user_id=data.user_id,
            role="assistant",
            message=response
        )

        db.add(user_message)
        db.add(ai_message)

        db.commit()

        return {
            "response": response
=======
from services.ai_service import AIService
from models.chat import ChatMessage

class ChatController:

    def __init__(self):
        self.ai = AIService()

    def send_message(self, db, data):

        response = self.ai.generate_response(
            data.message
        )

        user_message = ChatMessage(
            user_id=data.user_id,
            role="user",
            message=data.message
        )

        ai_message = ChatMessage(
            user_id=data.user_id,
            role="assistant",
            message=response
        )

        db.add(user_message)
        db.add(ai_message)

        db.commit()

        return {
            "response": response
>>>>>>> 1925e27 (Penambahan YOLO)
        }