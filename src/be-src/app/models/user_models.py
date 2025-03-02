from sqlalchemy import Boolean, Column, Integer, String, Enum, LargeBinary
from app.core.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)  # Họ tên
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(20), unique=True, nullable=False)  # Số điện thoại
    position = Column(String(100), nullable=False)  # Chức vụ
    profile_image = Column(String(255), nullable=False)  # Ảnh đại diện (lưu URL ảnh)
    username = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum("ADMIN", "USER", name="user_roles"), default="USER")  # Quyền
    status = Column(Enum("ACTIVE", "INACTIVE", name="user_statuses"), default="ACTIVE")  # Trạng thái
    email_verified = Column(Boolean, default=False)  # Mặc định là False
    # Quan hệ với các bảng khác
    attendances = relationship("Attendance", back_populates="user")
    notifications = relationship("Notification", back_populates="user")
    work_schedules = relationship("WorkSchedule", back_populates="user")

    otp_codes = relationship("OTPCode", back_populates="user", cascade="all, delete-orphan")
