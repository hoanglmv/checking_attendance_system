from pydantic import BaseModel, EmailStr, field_validator, validator
from typing import Optional
from enum import Enum

# Enum cho quyền và trạng thái user
class AttendanceStatus(str, Enum): 
    ON_TIME = "ON_TIME"
    LATE = "LATE"
    ABSENT = "ABSENT"
    ABSENT_WITH_PERMISSION = "ABSENT_WITH_PERMISSION"

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

    @field_validator('full_name', 'phone', 'position', 'department', mode='before')
    def strip_strings(cls, value):
        if isinstance(value, str):
            return value.strip()
        return value

# Schema phản hồi khi lấy thông tin user
class AdminResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone: str
    position: str
    department: str

    class Config:
        from_attributes = True  # Cho phép chuyển đổi từ SQLAlchemy model

class EmployeeSearch(BaseModel):
    employee_code: str

class AttendanceCreate(BaseModel):
    employee_code: str
    date: str # Format: YYYY-MM-DD
    status: AttendanceStatus

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    email: EmailStr
    otp: str
    new_password: str
    confirm_password: str

    @field_validator('new_password')
    def password_length(cls, v):
        if len(v) < 8:  # Cập nhật thành 8 ký tự
            raise ValueError('Password must be at least 8 characters')
        return v

    @field_validator('confirm_password')
    def passwords_match(cls, v, info):
        if 'new_password' in info.data and v != info.data['new_password']:
            raise ValueError('Passwords do not match')
        return v