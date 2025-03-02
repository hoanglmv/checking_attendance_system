from pydantic import BaseModel
from datetime import datetime

class AttendanceCreate(BaseModel):
    user_id: int
    check_in: datetime
