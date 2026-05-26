from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from database.connection import Base


class SessionData(Base):
    __tablename__ = "session_data"

    session_id         = Column(Integer,     primary_key=True, index=True)
    user_id            = Column(Integer)
    method_type        = Column(String(50))
    duration           = Column(Integer)
    drowsy_count       = Column(Integer,     default=0)
    monitoring_enabled = Column(Boolean,     default=False)
    chat_session_id    = Column(String(100), nullable=True)
    timestamp          = Column(DateTime,    default=datetime.utcnow)