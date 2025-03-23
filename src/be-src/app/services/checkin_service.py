from sqlalchemy.orm import Session
from app.models.attendance import Attendance
from app.schemas.checkin_schema import AttendanceCreate, AttendanceUpdate

def create_checkin(db: Session, data: AttendanceCreate) -> Attendance:
    """Tạo bản ghi attendance mới (điểm danh)."""
    new_attendance = Attendance(
        employee_code=data.employee_code,
        date=data.date,
        check_in_time=data.check_in_time,
        check_out_time=data.check_out_time,
        is_late=data.is_late,
        is_absent=data.is_absent,
        is_permission_absent=data.is_permission_absent
    )
    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)
    return new_attendance

def update_checkin(db: Session, attendance_id: int, data: AttendanceUpdate) -> Attendance:
    """Cập nhật bản ghi attendance theo ID."""
    attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    if not attendance:
        return None  # hoặc raise HTTPException(404, "Attendance not found")

    # Chỉ cập nhật các trường không None
    if data.check_out_time is not None:
        attendance.check_out_time = data.check_out_time
    if data.is_late is not None:
        attendance.is_late = data.is_late
    if data.is_absent is not None:
        attendance.is_absent = data.is_absent
    if data.is_permission_absent is not None:
        attendance.is_permission_absent = data.is_permission_absent

    db.commit()
    db.refresh(attendance)
    return attendance

def get_checkin_by_id(db: Session, attendance_id: int) -> Attendance:
    """Lấy bản ghi attendance theo ID."""
    return db.query(Attendance).filter(Attendance.id == attendance_id).first()

def get_all_checkins(db: Session) -> list[Attendance]:
    """Lấy tất cả bản ghi attendance."""
    return db.query(Attendance).all()
