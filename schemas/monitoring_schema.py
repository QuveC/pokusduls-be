from pydantic import BaseModel

class MonitoringRequest(BaseModel):
    session_id: int