import os
import pickle
import numpy as np
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.employees import Employee 
# Tạo session để thao tác với database
db: Session = SessionLocal()

# Đường dẫn đến file .pkl
file_path = os.path.join("data", "embedding", "00003.pkl")

# Đọc dữ liệu từ file .pkl
with open(file_path, "rb") as f:
    face_data = pickle.load(f)  # Đây là numpy.ndarray

# Chuyển numpy.ndarray thành bytes để lưu vào LargeBinary
face_embedding_bytes = face_data.tobytes()

# Thêm nhân viên vào database
new_employee = Employee(
    employee_code="00003",
    full_name="Hung Minh Tuan",
    position="Software Engineer",
    department="Embedded",
    email="22020003@vnu.edu.vn",
    phone="0912341432",
    face_embedding=face_embedding_bytes  # Dữ liệu đã chuyển thành bytes
)

# Lưu vào database
db.add(new_employee)
db.commit()
db.close()

print("Dữ liệu đã được lưu thành công!")