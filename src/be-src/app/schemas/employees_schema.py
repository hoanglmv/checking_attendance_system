from pydantic import BaseModel, EmailStr
from typing import Optional

#Tạo nhân viên mới 
class EmployeeCreate(BaseModel):
    employee_code: str
    full_name: str
    position: str
    department: str
    email: EmailStr
    phone: str

#Cập nhật thông tin nhân viên
class EmployeeUpdate(BaseModel):
    full_name: Optional[str] = None
    position: Optional[str] = None
    department: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

#Get thông tin nhân viên
class EmployeeResponse(BaseModel):
    id: int
    employee_code: str
    full_name: str
    position: str
    department: str
    email: EmailStr
    phone: str

    class Config:
        from_attributes = True