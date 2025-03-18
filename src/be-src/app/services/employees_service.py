from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.employees import Employee
from app.schemas.employees_schema import EmployeeCreate, EmployeeUpdate


# Add nhân viên
def create_employee(db: Session, employee_data: EmployeeCreate):
    employee_data_dict = employee_data.model_dump(exclude={"employee_code"})  # Bỏ employee_code ra khỏi input
    employee_code = generate_employee_code(db)  # Tự động tạo mã nhân viên
    employee_data_dict["employee_code"] = employee_code  # Gán mã nhân viên vào dữ liệu

    employee = Employee(**employee_data_dict)
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee

# Lấy danh sách all nhân viên
def get_all_employees(db: Session):
    return db.query(Employee).all()

# Get nhân viên theo mã nhân viên
def get_employee_by_code(db: Session, employee_code: str):
    return db.query(Employee).filter(Employee.employee_code == employee_code).first()

# Update thông tin nhân viên theo má nhân viên
def update_employee(db: Session, employee_code: str, employee_data: EmployeeUpdate):
    employee = get_employee_by_code(db, employee_code)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    update_data = employee_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(employee, key, value)

    db.commit()
    db.refresh(employee)
    return employee

# Delete nhân viên
def delete_employee(db: Session, employee_code: str):
    employee = get_employee_by_code(db, employee_code)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

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

