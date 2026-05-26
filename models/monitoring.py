from sqlalchemy import Column, Integer, DateTime, Boolean
from datetime import datetime
from database.connection import Base


class MonitoringSession(Base):
    __tablename__ = "monitoring_session"

    monitoring_id = Column(Integer,  primary_key=True)
    session_id    = Column(Integer)
    start_time    = Column(DateTime, default=datetime.utcnow)
    end_time      = Column(DateTime, nullable=True)
    drowsy_events = Column(Integer,  default=0)
    total_alerts  = Column(Integer,  default=0)
    is_active     = Column(Boolean,  default=True)