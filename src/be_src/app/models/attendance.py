# E:\AttendanceCheckingApp\checking_attendance_system\src\be_src\app\models\attendance.py
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Attendance(Base):
    __tablename__ = "attendances"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    employee_code = Column(String(255), ForeignKey("employees.employee_code"), nullable=False)  # Sửa lại khóa ngoại
    date = Column(Date, nullable = False)  # Ngày điểm danh
    check_in_time = Column(DateTime, default=None, nullable=False)  # Giờ check-in
    check_out_time = Column(DateTime, default=None)  # Giờ check-out
    is_late = Column(Boolean, default=False)  # Đi muộn
    is_absent = Column(Boolean, default=False)  # Vắng mặt
    is_permission_absent = Column(Boolean, default=False)  # Xin phép nghỉ

    employee = relationship("Employee", back_populates="attendances")
