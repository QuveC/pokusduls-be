from sqlalchemy import Column, Integer, Float, Date
from database.connection import Base


class Statistics(Base):
    __tablename__ = "statistics"

    statistics_id     = Column(Integer, primary_key=True)
    user_id           = Column(Integer)
    total_xp          = Column(Integer, default=0)
    current_streak    = Column(Integer, default=0)   # diagram: currentStreak
    total_sessions    = Column(Integer, default=0)
    total_drowsy_events = Column(Integer, default=0) # diagram: totalDrowsyEvents
    avg_focus_score   = Column(Float,   default=0.0) # diagram: avgFocusScore
    chat_interactions = Column(Integer, default=0)   # diagram: chatInteractions
    last_active_date  = Column(Date,    nullable=True)
