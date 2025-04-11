# E:\AttendanceCheckingApp\checking_attendance_system\src\be_src\app\services\attendance_service.py
from fastapi import HTTPException
from sqlalchemy import distinct, extract
from sqlalchemy.orm import Session
from app.models.attendance import Attendance
from app.schemas.attendance_schema import AttendanceCreate, AttendanceResponse, AttendanceUpdate, AttendanceMonthlyResponse
from datetime import datetime, timedelta, date
from app.services.notification_service import send_notification
from app.models.employees import Employee
import calendar

# Thời gian quy định
CHECK_IN_TIME = datetime.strptime("08:00:00", "%H:%M:%S").time()
LATE_THRESHOLD = timedelta(minutes=15)
ABSENT_THRESHOLD = timedelta(hours=1)

# Check in
def check_in_employee(db: Session, attendance_data: AttendanceCreate):
    now = datetime.now()

    employee = db.query(Employee).filter(Employee.id == attendance_data.employee_id).first()
    if not employee:
        return {"error": "Employee not found"}, 404
    
    today = now.date()
    existing_attendance = (
        db.query(Attendance)
        .filter(Attendance.employee_code == employee.employee_code)
        .filter(Attendance.date == today)
        .first()
    )

    if existing_attendance:
        return {"error": "Employee has already checked in today"}, 400

    check_in_datetime = datetime.combine(today, now.time())
    check_in_threshold = datetime.combine(today, CHECK_IN_TIME) + LATE_THRESHOLD
    absent_threshold = datetime.combine(today, CHECK_IN_TIME) + ABSENT_THRESHOLD

    if check_in_datetime > ABSENT_THRESHOLD:
        is_late = False
        is_absent = True
    elif check_in_datetime > LATE_THRESHOLD:
        is_late = True
        is_absent = False
    else:
        is_late = False
        is_absent = False

    new_attendance = Attendance(
        employee_code=employee.employee_code,
        check_in_time=now,
        date=today,  # Lưu ngày vào cột date
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
        employee_id=employee.id,
        full_name=employee.full_name,
        position=employee.position,
        department=employee.department,
        check_in_time=new_attendance.check_in_time,
        is_late=new_attendance.is_late,
        is_absent=new_attendance.is_absent,
        is_permission_absent=new_attendance.is_permission_absent
    )

# Get danh sách điểm danh theo ngày 
def get_attendance_by_date(db: Session, date: datetime):
    try:
        # Chuyển đổi date thành định dạng date
        attendance_date = date.date()

        # Lấy tất cả nhân viên từ bảng employees
        employees = db.query(Employee).all()
        if not employees:
            return {
                "summary": {
                    "total_employees": 0,
                    "total_late": 0,
                    "total_absent_with_permission": 0,
                    "total_absent_without_permission": 0
                },
                "departments": {}
            }

        # Lấy dữ liệu điểm danh cho ngày được chọn
        attendances = (
            db.query(Attendance)
            .filter(Attendance.date == attendance_date)
            .all()
        )

        # Tạo dictionary để ánh xạ employee_code với thông tin điểm danh
        attendance_dict = {att.employee_code: att for att in attendances}

        # Nhóm nhân viên theo phòng ban
        departments = {}
        total_late = 0
        total_absent_with_permission = 0
        total_absent_without_permission = 0

        for emp in employees:
            department = emp.department if emp.department else "Không xác định"
            if department not in departments:
                departments[department] = []

            # Lấy thông tin điểm danh (nếu có)
            att = attendance_dict.get(emp.employee_code)
            employee_data = {
                "employee_id": emp.id,
                "employee_code": emp.employee_code,
                "full_name": emp.full_name,
                "position": emp.position,
                "check_in_time": att.check_in_time.strftime("%H:%M:%S") if att and att.check_in_time else None,
                "check_out_time": att.check_out_time.strftime("%H:%M:%S") if att and att.check_out_time else None,
                "late": att.is_late if att else False,
                "absent_with_permission": att.is_permission_absent if att else False,
                "absent_without_permission": att.is_absent if att else False
            }

            departments[department].append(employee_data)

            # Cập nhật thống kê
            if att:
                if att.is_late:
                    total_late += 1
                if att.is_permission_absent:
                    total_absent_with_permission += 1
                if att.is_absent:
                    total_absent_without_permission += 1

        total_employees = len(employees)

        return {
            "summary": {
                "total_employees": total_employees,
                "total_late": total_late,
                "total_absent_with_permission": total_absent_with_permission,
                "total_absent_without_permission": total_absent_without_permission
            },
            "departments": departments
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi lấy dữ liệu điểm danh: {str(e)}")

# Get thông tin điểm danh theo tháng của một nhân viên 
def get_attendance_by_month(db: Session, employee_id: int, month: int, year: int):
    try:
        # Lấy thông tin nhân viên dựa trên employee_id
        employee = db.query(Employee).filter(Employee.id == employee_id).first()
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")

        # Xác định ngày bắt đầu và kết thúc của tháng
        _, days_in_month = calendar.monthrange(year, month)
        month_start = date(year, month, 1)
        month_end = date(year, month, days_in_month)

        # Lấy start_date của nhân viên
        start_date = employee.start_date
        # Nếu start_date nằm ngoài tháng, điều chỉnh để chỉ lấy các ngày trong tháng
        start_date = max(start_date, month_start)
        end_date = month_end

        # Tạo danh sách các ngày từ start_date đến cuối tháng, loại bỏ thứ 7 và CN
        all_days = [month_start + timedelta(days=x) for x in range((end_date - month_start).days + 1)]
        valid_days = [day for day in all_days if day >= start_date and day.weekday() < 5]

        # Lấy danh sách điểm danh trong tháng, từ start_date trở đi
        records = db.query(Attendance).filter(
            Attendance.employee_code == employee.employee_code,
            Attendance.date >= start_date,
            Attendance.date <= end_date,
            extract('month', Attendance.date) == month,
            extract('year', Attendance.date) == year
        ).all()

        # Tạo dictionary để tra cứu nhanh bản ghi điểm danh theo ngày
        attendance_dict = {record.date: record for record in records}

        late_days = []
        absent_days = []
        permission_absent_days = []
        on_time_days = []

        for day in valid_days:
            record = attendance_dict.get(day)
            day_str = day.strftime("%Y-%m-%d")
            
            if record:
                if record.is_absent:
                    absent_days.append(day_str)
                elif record.is_permission_absent:
                    permission_absent_days.append(day_str)
                elif record.is_late:
                    late_days.append(day_str)
                else:
                    on_time_days.append(day_str)
            else:
                # Nếu không có bản ghi, coi như vắng không phép
                absent_days.append(day_str)

        total_check_ins = len(records)
        total_late = len(late_days)
        total_absent = len(absent_days)
        total_permission_absent = len(permission_absent_days)
        total_on_time = len(on_time_days)

        return AttendanceMonthlyResponse(
            employee_id=employee.id,
            full_name=employee.full_name,
            total_check_ins=total_check_ins,
            total_late=total_late,
            total_absent=total_absent,
            total_permission_absent=total_permission_absent,
            total_on_time=total_on_time,
            late_days=late_days,
            absent_days=absent_days,
            permission_absent_days=permission_absent_days,
            on_time_days=on_time_days
        )
    except Exception as e:
        print(f"Error in get_attendance_by_month: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Sửa phương thức get_attendance_departments
def get_attendance_departments(db: Session, date: str = None):
    """
    Lấy danh sách các phòng ban duy nhất dựa trên bản ghi điểm danh trong bảng attendances.
    Nếu có date, lọc theo ngày được chỉ định.
    """
    try:
        query = (
            db.query(distinct(Employee.department))
            .join(Attendance, Attendance.employee_code == Employee.employee_code)
            .filter(Employee.department.isnot(None))
        )
        
        # Nếu có date, lọc theo ngày
        if date:
            try:
                attendance_date = datetime.strptime(date, "%Y-%m-%d").date()
                query = query.filter(Attendance.date == attendance_date)
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

        departments = query.all()
        result = [dept[0] for dept in departments]
        return result if result else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi lấy danh sách phòng ban: {str(e)}")