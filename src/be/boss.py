from personal import Personal
from manager import Manager
from employee import Employee

class Boss(Personal):
    def __init__(self, per_id, name, gmail, phone_number, profile_image=None):
        super().__init__(per_id, name, "Boss", gmail, phone_number, profile_image=profile_image)
        self._managers = []  # Danh sách quản lý
        self._employees = []  # Danh sách nhân viên không thuộc quản lý nào

    def add_manager(self, manager: Manager):
        """Thêm Manager vào danh sách quản lý"""
        self._managers.append(manager)

    def add_employee(self, employee: Employee):
        """Thêm nhân viên trực tiếp dưới quyền Boss (không có Manager quản lý)"""
        self._employees.append(employee)

    def show_structure(self, level=0):
        """Hiển thị cấu trúc tổ chức"""
        print("\t" * level + f"- {self} (Quản lý {len(self._managers)} Manager, {len(self._employees)} Nhân viên)")
        for manager in self._managers:
            manager.show_structure(level + 1)
        for emp in self._employees:
            emp.show_structure(level + 1)
