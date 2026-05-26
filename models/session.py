from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from database.connection import Base


class SessionData(Base):
    """Diagram: SessionData — duration, methodType, timestamp, chatSessionId, drowsyCount, monitoringEnabled"""
    __tablename__ = "sessions"

    session_id         = Column(Integer,  primary_key=True, index=True)
    user_id            = Column(Integer)
    method_type        = Column(String(50))                          # diagram: methodType
    duration           = Column(Integer)
    xp_earned          = Column(Integer)
    drowsy_count       = Column(Integer,  default=0)                 # diagram: drowsyCount
    monitoring_enabled = Column(Boolean,  default=False)             # diagram: monitoringEnabled
    chat_session_id    = Column(String(100), nullable=True)          # diagram: chatSessionId
    created_at         = Column(DateTime, default=datetime.utcnow)   # diagram: timestamp
