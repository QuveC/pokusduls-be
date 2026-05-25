<<<<<<< HEAD
from sqlalchemy import Column, Integer
from database.connection import Base


class Statistics(Base):

    __tablename__ = "statistics"

    statistics_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    total_xp = Column(Integer, default=0)
    streak = Column(Integer, default=0)
=======
from sqlalchemy import Column, Integer
from database.connection import Base


class Statistics(Base):

    __tablename__ = "statistics"

    statistics_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    total_xp = Column(Integer, default=0)
    streak = Column(Integer, default=0)
>>>>>>> 1925e27 (Penambahan YOLO)
    total_sessions = Column(Integer, default=0)