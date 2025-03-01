import sqlite3
import numpy as np
import json
from be.person import Employee
class Company:
    def __init__(self, db_path="company.db"):
        """
        Khởi tạo công ty với database SQLite
        """
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self._create_table()
    
    def _create_table(self):
        """Tạo bảng nhân viên nếu chưa có"""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                emp_id TEXT PRIMARY KEY,
                name TEXT,
                position TEXT,
                gmail TEXT,
                phone_number TEXT,
                face_embedding TEXT,
                profile_image TEXT
            )
        """)
        self.conn.commit()
    
    def add_employee(self, employee: Employee):
        """Thêm nhân viên vào database"""
        try:
            face_embedding_str = json.dumps(employee.face_embedding.tolist()) if employee.face_embedding.size > 0 else None
            self.cursor.execute("""
                INSERT INTO employees (emp_id, name, position, gmail, phone_number, face_embedding, profile_image)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (employee.emp_id, employee.name, employee.position, employee.gmail, employee.phone_number, 
                  face_embedding_str, employee.profile_image))
            self.conn.commit()
            print(f"Đã thêm nhân viên {employee.name} vào database.")
        except sqlite3.IntegrityError:
            print(f"Nhân viên với ID {employee.emp_id} đã tồn tại!")

    def get_all_employees(self):
        """Lấy danh sách nhân viên từ database"""
        self.cursor.execute("SELECT * FROM employees")
        employees = []
        for row in self.cursor.fetchall():
            emp_id, name, position, gmail, phone_number, face_embedding, profile_image = row
            face_embedding = np.array(json.loads(face_embedding)) if face_embedding else None
            employee = Employee(emp_id, name, position, gmail, phone_number, face_embedding, profile_image)
            employees.append(employee)
        return employees
    
    def close(self):
        """Đóng kết nối database"""
        self.conn.close()
