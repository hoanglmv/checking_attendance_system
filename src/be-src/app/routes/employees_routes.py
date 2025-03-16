import os
import shutil
from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile, status
from pydantic import EmailStr
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.services.employees_service import (
    create_employee, get_all_employees, get_employee_by_code, 
    update_employee, delete_employee, get_employees_by_department,
)
from app.schemas.employees_schema import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from app.utils.dependencies import get_current_admin
from app.models.employees import Employee


router = APIRouter(prefix="/employees", tags=["Employees"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Add nhân viên
@router.post("/create", status_code=status.HTTP_201_CREATED)
async def add_employee(
    full_name: str = Form(...),
    position: str = Form(...),
    department: str = Form(...),
    email: EmailStr = Form(...),
    phone: str = Form(...),
    file: UploadFile = None,  # File upload
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    # Nếu có file thì lưu vào thư mục uploads
    file_path = None
    if file:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    # Tạo nhân viên
    employee_data = EmployeeCreate(
        full_name=full_name,
        position=position,
        department=department,
        email=email,
        phone=phone
    )
    new_employee = create_employee(db, employee_data)

    return {
        "message": "Employee created successfully",
        "employee": new_employee,
        "file_path": file_path  # Trả về đường dẫn file nếu có
    }

# Admin: Lấy thông tin tất cả nhân viên 
@router.get("/getall", response_model=list[EmployeeResponse])
def get_all_employees(db: Session = Depends(get_db)):
    employees = db.query(Employee).all()
    return [EmployeeResponse.model_validate(emp) for emp in employees]

# Admin: Lấy nhân viên theo mã nhân viên
@router.get("/{employee_code}")
def get_employee(employee_code: str, db: Session = Depends(get_db), admin: dict = Depends(get_current_admin)):
    employee = get_employee_by_code(db, employee_code)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return EmployeeResponse.model_validate(employee)



# Admin: Cập nhật thông tin nhân viên
@router.put("/update/{employee_code}")
def edit_employee(employee_code: str, employee_update: EmployeeUpdate, db: Session = Depends(get_db), admin: dict = Depends(get_current_admin)):
    updated_employee = update_employee(db, employee_code, employee_update)
    if not updated_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return updated_employee

# Admin: Xóa nhân viên
@router.delete("/{employee_code}", status_code=status.HTTP_204_NO_CONTENT)
def remove_employee(employee_code: str, db: Session = Depends(get_db), admin: dict = Depends(get_current_admin)):
    deleted_employee = delete_employee(db, employee_code)
    if not deleted_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    

# Lấy danh sách nhân viên theo phòng ban
@router.get("/department/{department}")
def get_employees_by_department_route(department: str, db: Session = Depends(get_db), admin: dict = Depends(get_current_admin)):
    employees = get_employees_by_department(db, department)
    if not employees:
        raise HTTPException(status_code=404, detail="No employees found in this department")
    return employees
