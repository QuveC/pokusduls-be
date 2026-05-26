from sqlalchemy import Column, Integer, Float
from database.connection import Base


class Statistics(Base):
    __tablename__ = "user_statistics"

    stat_id             = Column(Integer, primary_key=True)
    user_id             = Column(Integer)
    total_xp            = Column(Integer, default=0)
    current_streak      = Column(Integer, default=0)
    total_drowsy_events = Column(Integer, default=0)
    avg_focus_score     = Column(Float,   default=0.0)
    chat_interactions   = Column(Integer, default=0)