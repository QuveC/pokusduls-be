from pydantic import BaseModel

class SessionCreate(BaseModel):
    user_id: int
    duration: int
    method_type: str