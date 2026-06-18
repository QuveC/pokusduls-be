from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from database.connection import Base


class User(Base):
    __tablename__ = "users"

    user_id                = Column(Integer,     primary_key=True, index=True)
    username               = Column(String(100), unique=True)
    email                  = Column(String(150), unique=True)
    password_hash          = Column(String(255))
    created_at             = Column(DateTime,    default=datetime.utcnow)
    is_premium             = Column(Boolean,     nullable=False, default=False)
    premium_activated_at   = Column(DateTime,    nullable=True,  default=None)
    premium_activated_by   = Column(String(100), nullable=True,  default=None)