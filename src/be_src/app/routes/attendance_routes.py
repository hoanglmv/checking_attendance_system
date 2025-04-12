# E:\AttendanceCheckingApp\checking_attendance_system\src\be_src\app\routes\attendance_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, time, timedelta
from app.core.database import SessionLocal
from app.models import Employee, Attendance
from app.schemas.attendance_schema import AttendanceResponse, AttendanceMonthlyResponse, AttendanceCreate, AttendanceUpdate
from app.utils.dependencies import get_current_admin
from app.services.attendance_service import check_in_employee, get_attendance_by_month, get_attendance_departments

from fastapi import status

router = APIRouter(prefix="/attendance", tags=["Attendance"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Nhân viên thực hiện điểm danh (quét Face ID)
@router.post("/", status_code=status.HTTP_201_CREATED)
def add_attendance(attendance_data: AttendanceCreate, db: Session = Depends(get_db), admin: dict = Depends(get_current_admin)):
    return check_in_employee(db, attendance_data)

# ✅ API: Lấy danh sách điểm danh theo ngày
@router.get("/daily")
def get_attendance_by_date(
    date: str, db: Session = Depends(get_db), admin: dict = Depends(get_current_admin)
):
    try:
        attendance_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    # Lấy tất cả nhân viên trong DB
    employees = db.query(Employee).all()
    # Lấy bản ghi điểm danh trong ngày
    attendances = db.query(Attendance).filter(
        Attendance.check_in_time >= datetime.combine(attendance_date, datetime.min.time()),
        Attendance.check_in_time < datetime.combine(attendance_date + timedelta(days=1), datetime.min.time())
    ).all()

    department_data = {}
    total_present = 0
    total_absent_with_permission = 0
    total_absent_without_permission = 0
    total_late = 0

    # Tạo dictionary để tra cứu nhanh bản ghi điểm danh theo employee_code
    attendance_dict = {attendance.employee_code: attendance for attendance in attendances}

    for employee in employees:
        emp_attendance = attendance_dict.get(employee.employee_code)
        present = False
        late = False
        absent_with_permission = False
        absent_without_permission = False
        check_in_time = None

        if emp_attendance:
            present = True
            check_in_time = emp_attendance.check_in_time
            late = emp_attendance.is_late
            absent_with_permission = emp_attendance.is_permission_absent
            absent_without_permission = emp_attendance.is_absent

            if late:
                total_late += 1
            if absent_with_permission:
                total_absent_with_permission += 1
            if absent_without_permission:
                total_absent_without_permission += 1
            if not absent_with_permission and not absent_without_permission:
                total_present += 1
        else:
            # Nếu không có bản ghi điểm danh, đánh dấu là vắng không phép
            absent_without_permission = True
            total_absent_without_permission += 1

        if employee.department not in department_data:
            department_data[employee.department] = []

        department_data[employee.department].append({
            "employee_id": employee.id,
            "employee_code": employee.employee_code,
            "full_name": employee.full_name,
            "position": employee.position,
            "present": present,
            "check_in_time": check_in_time.strftime("%H:%M") if check_in_time else None,
            "late": late,
            "absent_with_permission": absent_with_permission,
            "absent_without_permission": absent_without_permission,
        })

    return {
        "date": date,
        "summary": {
            "total_employees": len(employees),
            "total_present": total_present,
            "total_absent_with_permission": total_absent_with_permission,
            "total_absent_without_permission": total_absent_without_permission,
            "total_late": total_late,
        },
        "departments": department_data
    }

# ✅ Xem danh sách điểm danh theo tháng của một nhân viên
@router.get("/{employee_id}/month/{year}/{month}", response_model=AttendanceMonthlyResponse)
def get_attendance_monthly(
    employee_id: int, year: int, month: int, db: Session = Depends(get_db), admin: dict = Depends(get_current_admin)
):
    return get_attendance_by_month(db, employee_id, month, year)

# ✅ API: Cập nhật thông tin điểm danh
# Thời gian quy định
CHECK_IN_TIME = time(8, 0, 0)  # 08:00:00
LATE_THRESHOLD = timedelta(minutes=15)
ABSENT_THRESHOLD = timedelta(hours=1)

@router.put("/update-attendance/{employee_id}")
def update_attendance_record(
    employee_id: int,
    update_data: AttendanceUpdate,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin),
):
    print(f"CHECK_IN_TIME: {CHECK_IN_TIME}")
    print(f"Nhận yêu cầu: employee_id={employee_id}, update_data={update_data.dict()}")

    attendance_date = update_data.date  # Đã được validator chuyển thành date
    is_late = update_data.is_late
    is_permission_absent = update_data.is_permission_absent
    is_absent = update_data.is_absent

    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    record = db.query(Attendance).filter(
        Attendance.employee_code == employee.employee_code,
        Attendance.date == attendance_date
    ).first()
    print(f"Bản ghi tìm thấy: {record.__dict__ if record else 'Không tìm thấy'}")

    if sum([is_late, is_absent, is_permission_absent]) > 1:
        raise HTTPException(status_code=400, detail="Only one of is_late, is_absent, or is_permission_absent can be True")

    if is_permission_absent:
        check_in_time = datetime.combine(attendance_date, datetime.min.time())
    elif is_absent:
        base_time = datetime.combine(attendance_date, CHECK_IN_TIME)
        check_in_time = base_time + ABSENT_THRESHOLD + timedelta(minutes=1)
    elif is_late:
        base_time = datetime.combine(attendance_date, CHECK_IN_TIME)
        check_in_time = base_time + LATE_THRESHOLD + timedelta(minutes=1)
    else:
        check_in_time = datetime.combine(attendance_date, CHECK_IN_TIME)

    print(f"check_in_time được tính toán: {check_in_time}")

    if not record:
        new_attendance = Attendance(
            employee_code=employee.employee_code,
            date=attendance_date,
            check_in_time=check_in_time,
            check_out_time=None,
            is_late=is_late,
            is_absent=is_absent,
            is_permission_absent=is_permission_absent
        )
        db.add(new_attendance)
        db.commit()
        db.refresh(new_attendance)
        print(f"Tạo bản ghi mới: {new_attendance.__dict__}")
        return {"message": "Attendance record created successfully"}, 201

    record.date = attendance_date
    record.check_in_time = check_in_time
    record.check_out_time = None
    record.is_late = is_late
    record.is_absent = is_absent
    record.is_permission_absent = is_permission_absent
    print(f"Trước khi commit: {record.__dict__}")
    db.commit()
    db.refresh(record)
    print(f"Sau khi commit: {record.__dict__}")

    return {"message": "Attendance record updated successfully"}, 200

# Sửa endpoint /attendance/departments
@router.get("/departments", response_model=list[str])
def get_attendance_departments_route(
    date: str = None,  # Thêm tham số date
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    """
    Lấy danh sách các phòng ban duy nhất dựa trên bản ghi điểm danh trong bảng attendances.
    Có thể lọc theo ngày nếu date được cung cấp (định dạng YYYY-MM-DD).
    """
    return get_attendance_departments(db, date)