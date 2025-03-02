from sqlalchemy.orm import Session
from app.models.attendance_model import Attendance
from app.schemas.attendance_schema import AttendanceCreate
from datetime import datetime

def create_attendance(db: Session, attendance: AttendanceCreate):
    db_attendance = Attendance(
        user_id=attendance.user_id,
        check_in=attendance.check_in,
        check_out=None
    )
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

def update_checkout(db: Session, user_id: int):
    attendance = db.query(Attendance).filter(Attendance.user_id == user_id, Attendance.check_out == None).first()
    if attendance:
        attendance.check_out = datetime.now()
        db.commit()
        return attendance
    return None
