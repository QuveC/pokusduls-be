from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database.connection import Base

class SessionData(Base):
    __tablename__ = "sessions"

    session_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    method_type = Column(String(50))
    duration = Column(Integer)
    xp_earned = Column(Integer)
    drowsy_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)