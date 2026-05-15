from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database.connection import Base

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    message_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    role = Column(String(50))
    message = Column(String(1000))
    created_at = Column(DateTime, default=datetime.utcnow)