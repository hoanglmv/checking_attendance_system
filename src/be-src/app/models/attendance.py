from sqlalchemy import Column, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base
import datetime

class Attendance(Base):
    __tablename__ = "attendances"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)  # Nhân viên điểm danh
    check_in_time = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))  
    is_late = Column(Boolean, default=False)  
    is_absent = Column(Boolean, default=False)  
    is_permission_absent = Column(Boolean, default=False)  

    employee = relationship("Employee", back_populates="attendances")
