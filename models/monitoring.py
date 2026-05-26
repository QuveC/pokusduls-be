from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean
from datetime import datetime
from database.connection import Base


class MonitoringSession(Base):
    """Diagram: MonitoringSession — startTime, drowsyEvents, totalAlerts"""
    __tablename__ = "monitoring_sessions"

    monitoring_id  = Column(Integer,  primary_key=True)
    session_id     = Column(Integer)
    start_time     = Column(DateTime, default=datetime.utcnow)  # diagram: startTime
    drowsy_events  = Column(Integer,  default=0)                # diagram: drowsyEvents
    total_alerts   = Column(Integer,  default=0)                # diagram: totalAlerts
    sleepy_detected = Column(Boolean, default=False)
    drowsy_count   = Column(Integer,  default=0)
