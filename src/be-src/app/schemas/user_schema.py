from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

# Enum cho quyền và trạng thái user
class UserRole(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"

class UserStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

# Schema tạo user mới
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    position: str
    profile_image: str
    face_embedding: bytes
    username: str
    password: str

# Schema đăng nhập
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Schema cập nhật user
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    position: Optional[str] = None
    profile_image: Optional[str] = None
    face_embedding: Optional[bytes] = None
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None
    status: Optional[UserStatus] = None

# Schema phản hồi khi lấy thông tin user
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    position: str
    profile_image: str
    username: str
    role: UserRole
    status: UserStatus

    class Config:
        from_attributes = True  # Cho phép chuyển đổi từ SQLAlchemy model
