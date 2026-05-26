from pydantic import BaseModel
from typing import Optional


class SessionCreate(BaseModel):
    user_id:            int
    duration:           int
    method_type:        str
    drowsy_count:       Optional[int]  = 0
    monitoring_enabled: Optional[bool] = False
    chat_session_id:    Optional[str]  = None
