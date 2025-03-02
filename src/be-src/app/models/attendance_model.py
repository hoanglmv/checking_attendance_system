from sqlalchemy import Column, Enum, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Attendance(Base):
    __tablename__ = "attendances"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    check_in = Column(DateTime, nullable=False)
    check_out = Column(DateTime, nullable=True)
    status = Column(Enum("ON_TIME", "LATE", name="attendance_status"), nullable=False)

    user = relationship("User", back_populates="attendances")
