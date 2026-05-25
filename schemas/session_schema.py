<<<<<<< HEAD
from pydantic import BaseModel

class SessionCreate(BaseModel):
    user_id: int
    duration: int
=======
from pydantic import BaseModel

class SessionCreate(BaseModel):
    user_id: int
    duration: int
>>>>>>> 1925e27 (Penambahan YOLO)
    method_type: str