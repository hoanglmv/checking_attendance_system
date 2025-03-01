from be.basic.person import Personal
from be.basic.employee import Employee

class Manager(Personal):
    def __init__(self, per_id, name, gmail, phone_number, profile_image=None):
        super().__init__(per_id, name, "Manager", gmail, phone_number, profile_image=profile_image)
        self._employees = []  # Danh sách nhân viên mà Manager quản lý

    def add_employee(self, employee: Employee):
        """Thêm nhân viên vào danh sách quản lý"""
        self._employees.append(employee)

    def remove_employee(self, employee_id):
        """Xóa nhân viên khỏi danh sách quản lý"""
        self._employees = [e for e in self._employees if e.per_id != employee_id]

    def show_structure(self, level=0):
        """Hiển thị cấu trúc quản lý"""
        print("\t" * level + f"- {self} (Quản lý {len(self._employees)} nhân viên)")
        for emp in self._employees:
            emp.show_structure(level + 1)
