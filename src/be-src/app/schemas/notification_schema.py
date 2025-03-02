from pydantic import BaseModel
from datetime import datetime

class NotificationCreate(BaseModel):
    message: str
    created_at: datetime
