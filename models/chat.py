from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from database.connection import Base


class ChatHistory(Base):
    __tablename__ = "chat_history"

    chat_history_id = Column(Integer,     primary_key=True)
    user_id         = Column(Integer)
    session_id      = Column(String(100))
    timestamp       = Column(DateTime,    default=datetime.utcnow)


class ChatMessage(Base):
    __tablename__ = "chat_message"

    message_id      = Column(Integer,  primary_key=True)
    chat_history_id = Column(Integer)
    role            = Column(String(20))
    content         = Column(Text)      # ← nama kolom di DB adalah 'content'
    timestamp       = Column(DateTime, default=datetime.utcnow)

    def toJSON(self):
        return {
            "role":      self.role,
            "content":   self.content,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
        }