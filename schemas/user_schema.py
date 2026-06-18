from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserRegister(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class PremiumStatusResponse(BaseModel):
    is_premium: bool
    premium_activated_at: Optional[datetime]

class ActivatePremiumRequest(BaseModel):
    user_id: int

class ActivatePremiumResponse(BaseModel):
    message: str
    user_id: int
    is_premium: bool
    activated_at: Optional[datetime]