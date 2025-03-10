from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class AttendanceCreate(BaseModel):
    employee_id: int
    check_in_time: Optional[datetime] = None
    is_late: bool = False
    is_absent: bool = False
    is_permission_absent: bool = False

class AttendanceUpdate(BaseModel):
    is_late: bool
    is_absent: bool
    is_permission_absent: bool

class AttendanceResponse(BaseModel):
    id: int
    employee_id: int
    full_name: str
    position: str
    department: str
    check_in_time: datetime
    is_late: bool
    is_absent: bool
    is_permission_absent: bool

    class Config:
        from_attributes = True
        
class AttendanceMonthlyResponse(BaseModel): 
    employee_id: int
    full_name: str
    total_check_ins: int
    total_late: int
    total_absent: int
    total_permission_absent: int
    late_days: List[datetime]
    absent_days: List[datetime]
    permission_absent_days: List[datetime]

class AttendanceDailyResponse(BaseModel):
    department: str
    total_employees: int
    present_count: int
    late_count: int
    absent_count: int
    permission_absent_count: int
    employees: List[AttendanceResponse]

