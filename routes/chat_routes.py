from fastapi import APIRouter
from database.connection import SessionLocal
from controllers.chat_controller import ChatController
from schemas.chat_schema import ChatRequest

router = APIRouter()

controller = ChatController()


@router.post("/chat/send")
def send_message(data: ChatRequest):

    db = SessionLocal()

    try:
        return controller.send_message(db, data)

    finally:
        db.close()