from typing import List, Optional
from pydantic import BaseModel, field_validator, validator
from datetime import datetime, date

class AttendanceCreate(BaseModel):
    employee_id: int
    date: date
    check_in_time: Optional[datetime] = None
    is_late: bool = False
    is_absent: bool = False
    is_permission_absent: bool = False

class AttendanceUpdate(BaseModel):
    date: str  # Nhận date dưới dạng chuỗi từ giao diện
    is_late: bool
    is_absent: bool
    is_permission_absent: bool

    @field_validator("date")  # Sử dụng field_validator thay vì validator
    @classmethod
    def validate_date(cls, value):
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD")

class AttendanceResponse(BaseModel):
    id: int
    employee_id: int
    full_name: str
    position: str
    department: str
    date: date
    check_in_time: Optional[datetime] = None
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
    total_on_time: int
    late_days: List[str]  # Sửa từ List[datetime] thành List[str]
    absent_days: List[str]  # Sửa từ List[datetime] thành List[str]
    permission_absent_days: List[str]  # Sửa từ List[datetime] thành List[str]
    on_time_days: List[str]  # Sửa từ List[datetime] thành List[str]

    class Config:
        from_attributes = True

class AttendanceDailyResponse(BaseModel):
    department: str
    total_employees: int
    present_count: int
    late_count: int
    absent_count: int
    permission_absent_count: int
    employees: List[AttendanceResponse]

