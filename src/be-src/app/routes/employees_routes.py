import os
from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile, File, status
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

# Add nhân viên
@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=EmployeeResponse)
async def add_employee(
    full_name: str = Form(...),
    position: str = Form(...),
    department: str = Form(...),
    email: EmailStr = Form(...),
    phone: str = Form(...),
    file: UploadFile = File(None),  # File upload (không bắt buộc)
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    # Tạo dữ liệu nhân viên từ form
    employee_data = EmployeeCreate(
        full_name=full_name,
        position=position,
        department=department,
        email=email,
        phone=phone
    )
    
    # Gọi service để tạo nhân viên và xử lý upload ảnh
    new_employee = await create_employee(db, employee_data, file)
    
    return new_employee

# Admin: Lấy thông tin tất cả nhân viên 
@router.get("/getall", response_model=list[EmployeeResponse])
def get_all_employees_route(db: Session = Depends(get_db)):
    employees = get_all_employees(db)
    return employees

# Admin: Lấy nhân viên theo mã nhân viên
@router.get("/get_employee/{employee_code}", response_model=EmployeeResponse)
def get_employee(employee_code: str, db: Session = Depends(get_db), admin: dict = Depends(get_current_admin)):
    employee = get_employee_by_code(db, employee_code)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

# Admin: Cập nhật thông tin nhân viên
@router.put("/update/{employee_code}", response_model=EmployeeResponse)
async def edit_employee(
    employee_code: str,
    full_name: str = Form(None),
    position: str = Form(None),
    department: str = Form(None),
    email: EmailStr = Form(None),
    phone: str = Form(None),
    file: UploadFile = File(None),  # File upload (không bắt buộc)
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    # Kiểm tra nếu full_name được cung cấp thì không được rỗng
    if full_name is not None and not full_name.strip():
        raise HTTPException(status_code=400, detail="Họ tên không được để trống")

    # Tạo dữ liệu cập nhật từ form
    employee_data = EmployeeUpdate(
        full_name=full_name,
        position=position,
        department=department,
        email=email,
        phone=phone
    )
    
    # Gọi service để cập nhật nhân viên và xử lý upload ảnh
    updated_employee = await update_employee(db, employee_code, employee_data, file)
    return updated_employee

# Admin: Xóa nhân viên
@router.delete("/{employee_code}", status_code=status.HTTP_204_NO_CONTENT)
def remove_employee(employee_code: str, db: Session = Depends(get_db), admin: dict = Depends(get_current_admin)):
    deleted_employee = delete_employee(db, employee_code)
    if not deleted_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return None

# Lấy danh sách nhân viên theo phòng ban
@router.get("/department/{department}", response_model=list[EmployeeResponse])
def get_employees_by_department_route(department: str, db: Session = Depends(get_db), admin: dict = Depends(get_current_admin)):
    employees = get_employees_by_department(db, department)
    if not employees:
        raise HTTPException(status_code=404, detail="No employees found in this department")
    return employees 

# Admin: Lấy danh sách các department 
@router.get("/departments", response_model=list[str])
def get_all_departments(db: Session = Depends(get_db), admin: dict = Depends(get_current_admin)):
    # Lấy tất cả các department từ cơ sở dữ liệu
    departments = db.query(Employee.department).distinct().all()
    # Trả về danh sách các department (loại bỏ None và chuyển thành list[str])
    return [dept[0] for dept in departments if dept[0] is not None]