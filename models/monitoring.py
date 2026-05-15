from sqlalchemy import Column, Integer, Boolean
from database.connection import Base

class MonitoringSession(Base):
    __tablename__ = "monitoring_sessions"

    monitoring_id = Column(Integer, primary_key=True)
    session_id = Column(Integer)
    sleepy_detected = Column(Boolean, default=False)
    drowsy_count = Column(Integer, default=0)