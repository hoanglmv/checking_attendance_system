import numpy as np
import pickle
from database import Database

class EmployeeController:
    def __init__(self):
        self.db = Database()

    def add_employee(self, name, email, phone, position, profile_image, face_embedding):
        """Thêm nhân viên mới vào cơ sở dữ liệu"""
        embedding_blob = pickle.dumps(face_embedding)
        query = """
        INSERT INTO employees (name, email, phone, position, profile_image, face_embedding)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.db.execute(query, (name, email, phone, position, profile_image, embedding_blob))

    def get_all_employees(self):
        """Lấy danh sách tất cả nhân viên"""
        query = "SELECT id, name, email, phone, position, profile_image FROM employees"
        return self.db.fetch(query)

    def get_employee_by_id(self, emp_id):
        """Lấy thông tin một nhân viên theo ID"""
        query = "SELECT id, name, email, phone, position, profile_image FROM employees WHERE id = %s"
        result = self.db.fetch(query, (emp_id,))
        return result[0] if result else None

    def update_employee(self, emp_id, name=None, email=None, phone=None, position=None, profile_image=None):
        """Cập nhật thông tin nhân viên"""
        query = "UPDATE employees SET "
        updates = []
        params = []
        
        if name:
            updates.append("name = %s")
            params.append(name)
        if email:
            updates.append("email = %s")
            params.append(email)
        if phone:
            updates.append("phone = %s")
            params.append(phone)
        if position:
            updates.append("position = %s")
            params.append(position)
        if profile_image:
            updates.append("profile_image = %s")
            params.append(profile_image)

        if not updates:
            return "Không có dữ liệu để cập nhật."

        query += ", ".join(updates) + " WHERE id = %s"
        params.append(emp_id)

        self.db.execute(query, tuple(params))

    def delete_employee(self, emp_id):
        """Xóa nhân viên khỏi cơ sở dữ liệu"""
        query = "DELETE FROM employees WHERE id = %s"
        self.db.execute(query, (emp_id,))
