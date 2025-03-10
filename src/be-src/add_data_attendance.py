import os
import pickle
import numpy as np
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.employees import Employee 
from app.models.attendance import Attendance
# Tạo session để thao tác với database
db: Session = SessionLocal()


# Thêm nhân viên vào database
new_employee = Attendance(
    employee_code="00004",
)

# Lưu vào database
db.add(new_employee)
db.commit()
db.close()

print("Dữ liệu đã được lưu thành công!")
