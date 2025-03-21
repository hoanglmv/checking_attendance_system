import sys
import os
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QTabWidget, QMessageBox
from PyQt6.QtCore import Qt, QSettings
import requests

# Cấu hình encoding để hỗ trợ tiếng Việt
sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from fe.components.header import Header
from fe.components.sidebar import Sidebar
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1

# Import các thành phần từ các file khác
from pages.employee_list_ui import EmployeeListUI
from pages.employee_detail_ui import EmployeeDetailUI
from pages.add_employee_ui import AddEmployeeUI
from pages.utils import update_frame, load_image, add_new_employee

class Ui_informationUI(object):
    def setupUi(self, informationUI):
        informationUI.setObjectName("informationUI")
        informationUI.setMinimumSize(1280, 720)
        informationUI.resize(1280, 720)
        informationUI.setStyleSheet("""
            background-color: #0B121F;
            border: none;
            font-family: 'Segoe UI', Arial, sans-serif;
        """)
        
        self.centralwidget = QtWidgets.QWidget(parent=informationUI)
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        
        # Sidebar
        self.sidebar = Sidebar(parent=self.centralwidget)
        self.sidebar.fil_attendance.setStyleSheet("border-radius: 5px; background-color: #1E2A38;")
        self.sidebar.fil_manage.setStyleSheet("background-color: #68D477; border-radius: 5px;")
        self.horizontalLayout.addWidget(self.sidebar)
        
        # Main Container
        self.main = QGroupBox(parent=self.centralwidget)
        self.main.setStyleSheet("background-color: #0B121F; border: none;")
        self.mainLayout = QVBoxLayout(self.main)
        self.mainLayout.setContentsMargins(10, 10, 10, 10)
        self.mainLayout.setSpacing(8)
        
        # Header
        self.header = Header(parent=self.main)
        self.mainLayout.addWidget(self.header)

        # Tab Widget
        self.tabWidget = QTabWidget()
        self.tabWidget.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #1E2A38;
                background: #0B121F;
                border-radius: 8px;
            }
            QTabBar::tab {
                background: #1E2A38;
                color: #C0C0C0;
                padding: 8px 16px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: 600;
                margin: 3px;
                transition: all 0.3s ease;
            }
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #68D477, stop:1 #4CAF50);
                color: black;
                font-size: 14px;
                border-bottom: 2px solid #4CAF50;
            }
            QTabBar::tab:hover {
                background: #2E3A4E;
                color: #A4F9C8;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            }
        """)
        self.mainLayout.addWidget(self.tabWidget)
        
        # Khởi tạo MTCNN và FaceNet
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.mtcnn = MTCNN(image_size=160, margin=10, keep_all=False, device=device)
        self.facenet = InceptionResnetV1(pretrained="vggface2").eval().to(device)

        # Tab 1: Thông tin nhân viên
        self.tab1 = QWidget()
        self.tab1Layout = QVBoxLayout(self.tab1)
        self.tab1Layout.setContentsMargins(0, 0, 0, 0)
        self.contentLayout = QHBoxLayout()
        self.contentLayout.setSpacing(15)
        self.contentLayout.setStretch(0, 1)
        self.contentLayout.setStretch(1, 2)
        self.tab1Layout.addLayout(self.contentLayout)
        self.tabWidget.addTab(self.tab1, "Thông tin nhân viên")
        
        # Employee List
        self.employee_list_ui = EmployeeListUI(self.contentLayout)
        self.employee_list_ui.employeeList.itemClicked.connect(self.displayEmployeeDetails)
        
        # Employee Detail
        self.employee_detail_ui = EmployeeDetailUI(self.contentLayout)
        self.employee_detail_ui.editButton.clicked.connect(self.toggleEditMode)
        self.employee_detail_ui.deleteButton.clicked.connect(self.delete_employee)  # Kết nối nút Xóa
        
        self.horizontalLayout.addWidget(self.main)
        informationUI.setCentralWidget(self.centralwidget)
        
        # Tab 2: Thêm nhân viên
        self.tab2 = QWidget()
        self.tabWidget.addTab(self.tab2, "Thêm nhân viên")
        self.add_employee_ui = AddEmployeeUI(self.tab2, self.mtcnn)
        self.add_employee_ui.loadImageButton.clicked.connect(lambda: load_image(self.add_employee_ui))
        self.add_employee_ui.saveButton2.clicked.connect(lambda: self.add_new_employee_safe())

        # Tải danh sách nhân viên từ API khi khởi động
        self.load_employees_from_api()

    def load_employees_from_api(self):
        """Tải danh sách nhân viên từ API"""
        settings = QSettings("MyApp", "LoginApp")
        access_token = settings.value("access_token")

        if not access_token:
            QMessageBox.critical(None, "Lỗi", "Không tìm thấy access_token. Vui lòng đăng nhập lại!")
            self.employees = []
        else:
            api_url = "http://127.0.0.1:8000/employees/getall"
            headers = {"Authorization": f"Bearer {access_token}"}
            try:
                response = requests.get(api_url, headers=headers)
                if response.status_code == 200:
                    self.employees = response.json()  # Danh sách nhân viên từ API
                    print("Đã tải danh sách nhân viên từ API!")
                else:
                    QMessageBox.warning(None, "Lỗi", f"Không thể tải danh sách nhân viên: {response.status_code} - {response.text}")
                    self.employees = []
            except requests.RequestException as e:
                QMessageBox.critical(None, "Lỗi", f"Không thể kết nối đến API: {str(e)}")
                self.employees = []

        self.employee_list_ui.populate_employee_list(self.employees)

    def add_new_employee_safe(self):
        """Gọi add_new_employee với xử lý ngoại lệ để tránh crash"""
        try:
            add_new_employee(self)
        except Exception as e:
            QMessageBox.critical(None, "Lỗi", f"Không thể thêm nhân viên: {str(e)}")
            
    def displayEmployeeDetails(self, item):
        """Hiển thị chi tiết nhân viên từ API"""
        emp = item.data(QtCore.Qt.ItemDataRole.UserRole)
        self.employee_detail_ui.lineEdits["Mã nhân viên:"].setText(emp.get('employee_code', ''))
        self.employee_detail_ui.lineEdits["Họ tên:"].setText(emp.get('full_name', ''))
        self.employee_detail_ui.lineEdits["Chức vụ:"].setText(emp.get('position', ''))
        self.employee_detail_ui.lineEdits["Nơi làm việc:"].setText(emp.get('department', ''))
        self.employee_detail_ui.lineEdits["Email:"].setText(emp.get('email', ''))
        self.employee_detail_ui.lineEdits["Số điện thoại:"].setText(emp.get('phone', ''))

        # Hiển thị ảnh avatar trong ô vuông
        avatar_url = emp.get('avatar_url')
        self.employee_detail_ui.set_avatar(avatar_url)

    def toggleEditMode(self):
        """Chuyển đổi chế độ chỉnh sửa và lưu thay đổi qua API"""
        self.isEditing = not getattr(self, 'isEditing', False)
        for key in self.employee_detail_ui.lineEdits:
            self.employee_detail_ui.lineEdits[key].setReadOnly(not self.isEditing)
        
        if self.isEditing:
            self.employee_detail_ui.editButton.setText("Lưu thay đổi")
            self.employee_detail_ui.editButton.setStyleSheet("""
                QPushButton {
                    background-color: #FFA500;
                    color: black;
                    padding: 8px 25px;
                    border-radius: 4px;
                    font-size: 14px;
                    font-weight: 600;
                    border: 1px solid #FFA500;
                    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
                    transition: all 0.3s ease;
                }
                QPushButton:hover {
                    background-color: #E69500;
                    border: 1px solid #E69500;
                    box-shadow: 0 3px 9px rgba(255, 165, 0, 0.4);
                    transform: scale(1.05);
                }
            """)
        else:
            self.save_employee_changes()
            self.employee_detail_ui.editButton.setText("Thay đổi thông tin")
            self.employee_detail_ui.editButton.setStyleSheet("""
                QPushButton {
                    background-color: #68D477;
                    color: black;
                    padding: 8px 25px;
                    border-radius: 4px;
                    font-size: 14px;
                    font-weight: 600;
                    border: 1px solid #68D477;
                    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
                    transition: all 0.3s ease;
                }
                QPushButton:hover {
                    background-color: #5AC469;
                    border: 1px solid #5AC469;
                    box-shadow: 0 3px 9px rgba(104, 212, 119, 0.4);
                    transform: scale(1.05);
                }
            """)

    def save_employee_changes(self):
        """Lưu thay đổi thông tin nhân viên qua API"""
        settings = QSettings("MyApp", "LoginApp")
        access_token = settings.value("access_token")

        if not access_token:
            QMessageBox.critical(None, "Lỗi", "Không tìm thấy access_token. Vui lòng đăng nhập lại!")
            return

        employee_code = self.employee_detail_ui.lineEdits["Mã nhân viên:"].text()
        update_data = {
            "full_name": self.employee_detail_ui.lineEdits["Họ tên:"].text(),
            "position": self.employee_detail_ui.lineEdits["Chức vụ:"].text(),
            "department": self.employee_detail_ui.lineEdits["Nơi làm việc:"].text(),
            "email": self.employee_detail_ui.lineEdits["Email:"].text(),
            "phone": self.employee_detail_ui.lineEdits["Số điện thoại:"].text(),
        }

        # Kiểm tra trường full_name không được rỗng
        if not update_data["full_name"].strip():
            QMessageBox.warning(None, "Lỗi", "Họ tên không được để trống!")
            return

        # Đảm bảo các trường khác không gửi None, mà gửi chuỗi rỗng nếu không có giá trị
        for key in update_data:
            if update_data[key] is None:
                update_data[key] = ""

        api_url = f"http://127.0.0.1:8000/employees/update/{employee_code}"
        headers = {"Authorization": f"Bearer {access_token}"}
        try:
            response = requests.put(api_url, data=update_data, headers=headers)  # Sử dụng data thay vì json để gửi Form
            if response.status_code == 200:
                QMessageBox.information(None, "Thành công", "Đã cập nhật thông tin nhân viên!")
                self.load_employees_from_api()  # Tải lại danh sách nhân viên sau khi cập nhật
            else:
                QMessageBox.warning(None, "Lỗi", f"Cập nhật thất bại: {response.status_code} - {response.text}")
        except requests.RequestException as e:
            QMessageBox.critical(None, "Lỗi", f"Không thể kết nối đến API: {str(e)}")
    def delete_employee(self):
        """Xóa nhân viên qua API"""
        settings = QSettings("MyApp", "LoginApp")
        access_token = settings.value("access_token")

        if not access_token:
            QMessageBox.critical(None, "Lỗi", "Không tìm thấy access_token. Vui lòng đăng nhập lại!")
            return

        employee_code = self.employee_detail_ui.lineEdits["Mã nhân viên:"].text()
        if not employee_code:
            QMessageBox.warning(None, "Lỗi", "Không tìm thấy mã nhân viên để xóa!")
            return

        # Xác nhận trước khi xóa
        reply = QMessageBox.question(None, "Xác nhận", f"Bạn có chắc chắn muốn xóa nhân viên {employee_code}?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply != QMessageBox.StandardButton.Yes:
            return

        # Sửa endpoint từ /employees/delete/{employee_code} thành /employees/{employee_code}
        api_url = f"http://127.0.0.1:8000/employees/{employee_code}"
        headers = {"Authorization": f"Bearer {access_token}"}
        try:
            response = requests.delete(api_url, headers=headers)
            if response.status_code == 204:  # Backend trả về 204 No Content
                QMessageBox.information(None, "Thành công", "Đã xóa nhân viên!")
                self.load_employees_from_api()  # Tải lại danh sách nhân viên sau khi xóa
                # Xóa nội dung chi tiết nhân viên
                for key in self.employee_detail_ui.lineEdits:
                    self.employee_detail_ui.lineEdits[key].clear()
                self.employee_detail_ui.photoLabel.setText("No Image")
            else:
                QMessageBox.warning(None, "Lỗi", f"Xóa thất bại: {response.status_code} - {response.text}")
        except requests.RequestException as e:
            QMessageBox.critical(None, "Lỗi", f"Không thể kết nối đến API: {str(e)}")
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    informationUI = QMainWindow()
    ui = Ui_informationUI()
    ui.setupUi(informationUI)
    informationUI.show()
    sys.exit(app.exec())