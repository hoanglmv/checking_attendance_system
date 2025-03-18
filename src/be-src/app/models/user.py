from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Enum, LargeBinary
from app.core.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)
    position = Column(String(255), nullable=True)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(255), nullable=True)  
    department = Column(String(255), nullable=False)  # Thêm dòng này
    email_verified = Column(Boolean, default=False)  
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    # Quan hệ với các bảng khác

    otp_codes = relationship("OTPCode", back_populates="user", cascade="all, delete-orphan")
