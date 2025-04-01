from fastapi import HTTPException, UploadFile
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.attendance import Attendance
from app.models.employees import Employee
from app.schemas.employees_schema import EmployeeCreate, EmployeeUpdate
import os
import unicodedata
import re

# Hàm chuẩn hóa tên file (không cần nữa nhưng giữ lại để tham khảo)
def normalize_filename(filename: str) -> str:
    # Chuyển ký tự tiếng Việt thành không dấu
    filename = ''.join(c for c in unicodedata.normalize('NFD', filename)
                      if unicodedata.category(c) != 'Mn')
    # Thay khoảng trắng bằng dấu gạch dưới
    filename = re.sub(r'\s+', '_', filename)
    # Loại bỏ ký tự đặc biệt, chỉ giữ lại chữ cái, số, dấu chấm và gạch dưới
    filename = re.sub(r'[^a-zA-Z0-9._-]', '', filename)
    return filename

# Thư mục lưu ảnh
UPLOAD_DIR = "be_src/app/uploads/avt_images"

# Add nhân viên
async def create_employee(db: Session, employee_data: EmployeeCreate, avatar_file: UploadFile = None):
    employee_data_dict = employee_data.model_dump(exclude={"employee_code"})  # Bỏ employee_code ra khỏi input
    employee_code = generate_employee_code(db)  # Tự động tạo mã nhân viên
    employee_data_dict["employee_code"] = employee_code  # Gán mã nhân viên vào dữ liệu

    print(f"Đang tạo nhân viên mới với mã: {employee_code}, dữ liệu: {employee_data_dict}")  # Thêm log

    employee = Employee(**employee_data_dict)

    # Xử lý upload ảnh nếu có
    if avatar_file:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        filename = f"avt_{employee_code}.jpg"
        file_path = os.path.join(UPLOAD_DIR, filename)
        print(f"Đang lưu ảnh tại: {file_path}")  # Thêm log
        with open(file_path, "wb") as f:
            content = await avatar_file.read()
            f.write(content)
        employee.avatar_url = f"avt_images/{filename}"

    db.add(employee)
    db.commit()
    db.refresh(employee)
    print(f"Đã tạo nhân viên thành công: {employee.employee_code}, start_date: {employee.start_date}")  # Thêm log
    return employee

# Lấy danh sách all nhân viên
def get_all_employees(db: Session):
    return db.query(Employee).all()

# Get nhân viên theo mã nhân viên
def get_employee_by_code(db: Session, employee_code: str):
    return db.query(Employee).filter(Employee.employee_code == employee_code).first()

# Update thông tin nhân viên theo mã nhân viên
async def update_employee(db: Session, employee_code: str, employee_data: EmployeeUpdate, avatar_file: UploadFile = None):
    employee = get_employee_by_code(db, employee_code)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Cập nhật các trường thông tin nhân viên chỉ khi giá trị không phải None và không rỗng
    update_data = employee_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if value is not None and (isinstance(value, str) and value.strip() or not isinstance(value, str)):
            setattr(employee, key, value)

    # Xử lý upload ảnh nếu có
    if avatar_file:
        # Xóa ảnh cũ nếu có
        if employee.avatar_url:
            old_file_path = os.path.join(UPLOAD_DIR, employee.avatar_url.split("/")[-1])
            if os.path.exists(old_file_path):
                os.remove(old_file_path)

        # Tạo thư mục app/data/uploads nếu chưa tồn tại
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        
        # Đặt tên file ảnh theo định dạng avt_{employee_code}.jpg
        filename = f"avt_{employee_code}.jpg"
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        # Lưu file vào uploads/avt_images
        with open(file_path, "wb") as f:
            content = await avatar_file.read()
            f.write(content)
        
        # Cập nhật avatar_url trong database
        employee.avatar_url = f"avt_images/{filename}"

    db.commit()
    db.refresh(employee)
    return employee

# Delete nhân viên
def delete_employee(db: Session, employee_code: str):
    employee = get_employee_by_code(db, employee_code)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.query(Attendance).filter(Attendance.employee_code == employee.employee_code).delete()
    # Xóa ảnh nếu có
    if employee.avatar_url:
        file_path = os.path.join(UPLOAD_DIR, employee.avatar_url.split("/")[-1])
        if os.path.exists(file_path):
            os.remove(file_path)

    db.delete(employee)
    db.commit()
    return employee

def generate_employee_code(db: Session):
    last_employee = db.query(func.max(Employee.id)).scalar()  # Lấy ID lớn nhất
    new_id = (last_employee or 0) + 1  # Nếu chưa có nhân viên nào, bắt đầu từ 1
    return f"25{new_id:05d}"  # Định dạng mã nhân viên (vd: 250001, 250002, ...)

# Lấy danh sách nhân viên theo phòng ban
def get_employees_by_department(db: Session, department: str):
    return db.query(Employee).filter(Employee.department == department).all()