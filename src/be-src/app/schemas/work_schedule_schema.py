from pydantic import BaseModel
from datetime import time

class WorkScheduleCreate(BaseModel):
    shift_name: str
    start_time: time
    end_time: time
