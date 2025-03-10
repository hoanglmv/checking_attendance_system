from sqlalchemy import extract
from sqlalchemy.orm import Session
from app.models.attendance import Attendance
from app.schemas.attendance_schema import AttendanceCreate, AttendanceResponse, AttendanceUpdate, AttendanceMonthlyResponse
from datetime import datetime, timedelta, timezone
from app.services.notification_service import send_notification  # Import thông báo

from app.models.employees import Employee

# Thời gian quy định
CHECK_IN_TIME = datetime.strptime("08:00:00", "%H:%M:%S").time()
LATE_THRESHOLD = timedelta(minutes=15)
ABSENT_THRESHOLD = timedelta(hours=1)

# Check in
def check_in_employee(db: Session, attendance_data: AttendanceCreate):
    now = datetime.now(timezone.utc)

    employee = db.query(Employee).filter(Employee.id == attendance_data.employee_id).first()
    if not employee:
        return {"error" : "Employee not found"}, 404
    
    today = now.date()
    existing_attendance = (
        db.query(Attendance)
        .filter(Attendance.employee_id == attendance_data.employee_id)
        .filter(Attendance.check_in_time >= datetime.combine(today, datetime.min.time()))
        .first()
    )

    if existing_attendance:
        return {"error": "Employee has already checked in today"}, 400

    is_late = now.time() > datetime.combine(today, CHECK_IN_TIME + LATE_THRESHOLD).time()
    is_absent = now.time() > datetime.combine(today, CHECK_IN_TIME + ABSENT_THRESHOLD).time()
    new_attendance = Attendance(
        employee_id=attendance_data.employee_id,
        check_in_time=now,
        is_late=is_late,
        is_absent=is_absent,
        is_permission_absent=False
    )

    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)

    # Gửi thông báo
    status = "Điểm danh đúng giờ"
    if is_late:
        status = "Điểm danh muộn"
    elif is_absent:
        status = "Vắng mặt"

    message = f"Nhân viên {employee.full_name} đã {status} vào lúc {now.strftime('%H:%M:%S')}"

    import asyncio
    asyncio.create_task(send_notification(message))

    return AttendanceResponse(
        id=new_attendance.id,
        employee_id=new_attendance.employee_id,
        full_name=employee.full_name,
        position=employee.position,
        department=employee.department,
        check_in_time=new_attendance.check_in_time,
        is_late=new_attendance.is_late,
        is_absent=new_attendance.is_absent,
        is_permission_absent=new_attendance.is_permission_absent
    )

# get danh sách điểm danh theo ngày 
def get_attendance_by_date(db: Session, date: datetime):
    records = db.query(Attendance).filter(
        extract("year", Attendance.check_in_time) == date.year,
        extract("month", Attendance.check_in_time) == date.month,
        extract("day", Attendance.check_in_time) == date.day
    ).all()

    if not records:
        return {"error": "No attendance records found for the selected date."}

    grouped_by_department = {}
    for record in records:
        employee = db.query(Employee).filter(Employee.id == record.employee_id).first()
        department = employee.department

        if department not in grouped_by_department:
            grouped_by_department[department] = {
                "department": department,
                "total_employees": 0,
                "present_count": 0,
                "late_count": 0,
                "absent_count": 0,
                "permission_absent_count": 0,
                "employees": []
            }

        grouped_by_department[department]["total_employees"] += 1
        if record.is_absent:
            grouped_by_department[department]["absent_count"] += 1
        elif record.is_permission_absent:
            grouped_by_department[department]["permission_absent_count"] += 1
        else:
            grouped_by_department[department]["present_count"] += 1
            if record.is_late:
                grouped_by_department[department]["late_count"] += 1

        grouped_by_department[department]["employees"].append(record)

    return list(grouped_by_department.values())


# Update thông tin điểm danh
def update_attendance(db: Session, employee_id: int, date: datetime):
    record = (
        db.query(Attendance)
        .filter(Attendance.employee_id == employee_id)
        .filter(Attendance.check_in_time >= datetime.combine(date, datetime.min.time()))
        .filter(Attendance.check_in_time < datetime.combine(date, datetime.max.time()))
        .first()
    )

    if not record:
        return {"error": "Attendance record not found"}

    record.is_permission_absent = True
    record.is_absent = False  # Khi vắng có phép thì không phải vắng không phép
    db.commit()
    db.refresh(record)

    return {"message": "Attendance record updated successfully"}, 200


# get thông tin điểm danh theo tháng của một nhân viên 
def get_attendance_by_month(db: Session, employee_id: int, month: int, year: int):
    # get danh sách điểm danh theo tháng
    records = db.query(Attendance).filter (
        Attendance.employee_id == employee_id,
        extract('month', Attendance.check_in_time) == month,
        extract('year', Attendance.check_in_time) == year
    ).all()

    if not records: 
        return {"error": "Attendance record not found"}, 404
    
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        return {"error": "Employee not found"}, 404

    total_check_ins = len(records)
    total_late = sum(1 for record in records if record.is_late)
    total_absent = sum(1 for record in records if record.is_absent)
    total_permission_absent = sum(1 for record in records if record.is_permission_absent)
    late_days = [record.check_in_time for record in records if record.is_late]
    absent_days = [record.check_in_time for record in records if record.is_absent]
    permission_absent_days = [record.check_in_time for record in records if record.is_permission_absent]

    return AttendanceMonthlyResponse(
        employee_id=employee_id,
        full_name=employee.full_name,
        total_check_ins=total_check_ins,
        total_late=total_late,
        total_absent=total_absent,
        total_permission_absent=total_permission_absent,
        late_days=late_days,
        absent_days=absent_days,
        permission_absent_days=permission_absent_days
    )

