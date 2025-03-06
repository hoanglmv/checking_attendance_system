from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.core.database import SessionLocal
from app.models import Employee, Attendance
from app.schemas.attendance_schema import AttendanceResponse, AttendanceMonthlyResponse, AttendanceCreate
from app.dependencies import get_current_admin
from app.services.attendance_service import check_in_employee, get_attendance_by_month, update_attendance

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

    # Lấy danh sách nhân viên theo phòng ban
    employees = db.query(Employee).all()
    attendances = db.query(Attendance).filter(Attendance.date == attendance_date).all()

    department_data = {}
    total_present = 0
    total_absent_with_permission = 0
    total_absent_without_permission = 0
    total_late = 0

    for employee in employees:
        emp_attendance = next((a for a in attendances if a.employee_id == employee.id), None)
        present = False
        late = False
        absent_with_permission = False
        absent_without_permission = False
        check_in_time = None

        if emp_attendance:
            present = True
            check_in_time = emp_attendance.check_in_time
            if check_in_time > datetime.combine(attendance_date, datetime.strptime("08:15", "%H:%M").time()):
                late = True
                total_late += 1
            if check_in_time > datetime.combine(attendance_date, datetime.strptime("09:00", "%H:%M").time()):
                absent_without_permission = True
                total_absent_without_permission += 1
            else:
                total_present += 1
        else:
            absent_with_permission = True  # Mặc định nếu không có bản ghi là vắng có phép
            total_absent_with_permission += 1

        if employee.department not in department_data:
            department_data[employee.department] = []

        department_data[employee.department].append({
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
    result = get_attendance_by_month(db, employee_id, year, month)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# ✅ API: Cập nhật thông tin điểm danh (chuyển từ vắng không phép -> vắng có phép)
@router.put("/update-attendance/{employee_id}")
def update_attendance_record(
    employee_id: int,
    date: str,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin),
):
    try:
        attendance_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    result = update_attendance(db, employee_id, attendance_date)
    
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    
    return result