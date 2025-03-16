from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

# Enum cho quyền và trạng thái user
class AttendanceStatus(str, Enum): 
    ON_TIME = "ON_TIME"
    LATE = "LATE"
    ABSENT = "ABSENT"
    ABSENT_WITH_PERMISSION = "ABSENT_WITH_PERMISSION"

class AdminStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

# Schema tạo user mới
class AdminCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    position: str
    department: str
    password: str

# Schema đăng nhập
class AdminLogin(BaseModel):
    email: EmailStr
    password: str

# Schema cập nhật user
class AdminUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    position: Optional[str] = None
    department: Optional[str] = None
    status: Optional[AdminStatus] = None

# Schema phản hồi khi lấy thông tin user
class AdminResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone: str
    position: str
    department: str
    status: AdminStatus

    class Config:
        from_attributes = True  # Cho phép chuyển đổi từ SQLAlchemy model
    

class EmployeeSearch(BaseModel):
    employee_code: str

class AttendanceCreate(BaseModel):
    employee_code: str
    date: str # Format: YYYY-MM-DD
    status: AttendanceStatus
