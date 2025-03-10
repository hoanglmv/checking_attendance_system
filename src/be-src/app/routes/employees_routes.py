from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.services.employees_service import (
    create_employee, get_all_employees, get_employee_by_code, 
    update_employee, delete_employee, get_employees_by_department,
)
from app.schemas.employees_schema import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from app.dependencies import get_current_admin
from app.models.employees import Employee


router = APIRouter(prefix="/employees", tags=["Employees"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Add nhân viên
@router.post("/", status_code=status.HTTP_201_CREATED)
def add_employee(employee: EmployeeCreate, db: Session = Depends(get_db), admin: dict = Depends(get_current_admin)):
    return create_employee(db, employee)


# Admin: Lấy nhân viên theo mã nhân viên
@router.get("/{employee_code}")
def get_employee(employee_code: str, db: Session = Depends(get_db), admin: dict = Depends(get_current_admin)):
    employee = get_employee_by_code(db, employee_code)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@router.get("/all", response_model=list[EmployeeResponse])
def get_all_employees(db: Session = Depends(get_db)):
    employees = db.query(Employee).all()
    return [EmployeeResponse.model_validate(emp) for emp in employees]

# Admin: Cập nhật thông tin nhân viên
@router.put("/{employee_code}")
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
