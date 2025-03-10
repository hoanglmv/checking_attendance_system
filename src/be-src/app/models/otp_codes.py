from sqlalchemy import Boolean, Column, Integer, String, Enum, LargeBinary, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

class OTPCode(Base):
    __tablename__ = "otp_codes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), ForeignKey("users.email"), nullable=False, index=True)
    otp = Column(String(6), nullable=False)  # Mã OTP 6 chữ số
    expires_at = Column(DateTime, nullable=False, default=lambda: datetime.utcnow())

    user = relationship("User", back_populates="otp_codes")

# Thêm quan hệ vào model User để liên kết với OTPCode
    user = relationship("User", back_populates="otp_codes")
