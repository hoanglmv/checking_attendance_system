from datetime import date
from pydantic import BaseModel, EmailStr
from typing import Optional

# Tạo nhân viên mới (ảnh đại diện có thể không cần)
class EmployeeCreate(BaseModel):
    full_name: str
    position: str
    department: str
    email: EmailStr
    phone: str
    avatar_url: Optional[str] = None  # Có thể không thêm ảnh ngay

# Cập nhật thông tin nhân viên (cho phép cập nhật ảnh)
class EmployeeUpdate(BaseModel):
    full_name: Optional[str] = None
    position: Optional[str] = None
    department: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None  # Thêm hoặc cập nhật ảnh đại diện

# Get thông tin nhân viên
class EmployeeResponse(BaseModel):
    id: int
    employee_code: str
    full_name: str
    position: str
    department: str
    email: EmailStr
    phone: str
    avatar_url: Optional[str] = None  # Trả về đường dẫn ảnh đại diện
    start_date: Optional[date] = None

    class Config:
        from_attributes = True
