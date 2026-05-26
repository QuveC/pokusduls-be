from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database.connection import Base


class ChatMessage(Base):
    """Diagram: ChatMessage — role, content, timestamp + toJSON()"""
    __tablename__ = "chat_messages"

    message_id  = Column(Integer,  primary_key=True)
    user_id     = Column(Integer)
    role        = Column(String(50))
    message     = Column(String(2000))   # renamed from 'content' but same field
    created_at  = Column(DateTime, default=datetime.utcnow)

    def toJSON(self):
        return {
            "role":      self.role,
            "content":   self.message,
            "timestamp": self.created_at.isoformat() if self.created_at else None,
        }
