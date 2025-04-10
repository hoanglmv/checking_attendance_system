import sys
import os
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QTabWidget, QMessageBox, QFileDialog, QPushButton
from PyQt6.QtCore import Qt, QSettings, QObject, pyqtSignal
from PyQt6.QtGui import QPixmap, QCursor
import requests

sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from fe.components.header import Header
from fe.components.sidebar import Sidebar
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1

from pages.employee_list_ui import EmployeeListUI
from pages.employee_detail_ui import EmployeeDetailUI
from pages.add_employee_ui import AddEmployeeUI
from pages.utils import update_frame, load_image, add_new_employee

class Ui_informationUI(QObject):
    logout_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

    def setupUi(self, informationUI, stacked_widget=None):
        self.stacked_widget = stacked_widget

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
        
        self.sidebar = Sidebar(parent=self.centralwidget, stacked_widget=self.stacked_widget)
        self.sidebar.fil_attendance.setStyleSheet("border-radius: 5px; background-color: #1B2B40;")
        self.sidebar.fil_manage.setStyleSheet("background-color: #68D477; border-radius: 5px;")
        self.horizontalLayout.addWidget(self.sidebar)
        
        self.main = QGroupBox(parent=self.centralwidget)
        self.main.setStyleSheet("background-color: #0B121F; border: none;")
        self.mainLayout = QVBoxLayout(self.main)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.mainLayout.setSpacing(8)
        
        self.header = Header(parent=self.main)
        self.mainLayout.addWidget(self.header)

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
                border-radius: 6px;
                font-size: 13px;
                font-weight: 600;
                margin: 2px 2px 8px 10px;
                min-width: 180px;
                min-height: 40px;
                max-width: 180px;
                max-height: 40px;
                transition: all 0.3s ease;
            }
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #68D477, stop:1 #4CAF50);
                color: black;
                font-size: 13px;
                border-bottom: 2px solid #4CAF50;
            }
            QTabBar::tab:hover {
                background: #2E3A4E;
                color: #A4F9C8;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            }
        """)
        self.mainLayout.addWidget(self.tabWidget)
        
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.mtcnn = MTCNN(image_size=160, margin=10, keep_all=False, device=device)
        self.facenet = InceptionResnetV1(pretrained="vggface2").eval().to(device)

        self.tab1 = QWidget()
        self.tab1Layout = QVBoxLayout(self.tab1)
        self.tab1Layout.setContentsMargins(0, 0, 0, 0)
        self.contentLayout = QHBoxLayout()
        self.contentLayout.setSpacing(15)
        self.contentLayout.setStretch(0, 1)
        self.contentLayout.setStretch(1, 2)
        self.tab1Layout.addLayout(self.contentLayout)
        self.tabWidget.addTab(self.tab1, "Thông tin nhân viên")
        
        self.employee_list_ui = EmployeeListUI(self.contentLayout)
        self.employee_list_ui.employeeList.itemClicked.connect(self.displayEmployeeDetails)
        
        self.employee_detail_ui = EmployeeDetailUI(self.contentLayout)
        self.employee_detail_ui.editButton.clicked.connect(self.toggleEditMode)
        self.employee_detail_ui.deleteButton.clicked.connect(self.delete_employee)
        self.employee_detail_ui.loadImageButton.clicked.connect(self.load_image_for_update)
        
        self.horizontalLayout.addWidget(self.main)
        
        informationUI.setLayout(self.horizontalLayout)
        
        self.tab2 = QWidget()
        self.tabWidget.addTab(self.tab2, "Thêm nhân viên")
        self.add_employee_ui = AddEmployeeUI(self.tab2, self.mtcnn)
        self.add_employee_ui.loadImageButton.clicked.connect(lambda: load_image(self.add_employee_ui))
        self.add_employee_ui.saveButton2.clicked.connect(lambda: self.add_new_employee_safe())

    def load_employees_from_api(self):
        print("Bắt đầu load_employees_from_api")
        try:
            settings = QSettings("MyApp", "LoginApp")
            access_token = settings.value("access_token")
            print(f"Token trong load_employees_from_api trước khi gọi API: {access_token}")

            if not access_token:
                print("Không tìm thấy access_token trong load_employees_from_api")
                self.employees = []
                self.employee_list_ui.populate_employee_list(self.employees)
                if self.stacked_widget:
                    self.logout_signal.emit()
                return

            api_url = "http://127.0.0.1:8000/employees/getall"
            headers = {"Authorization": f"Bearer {access_token}"}
            print("Gửi yêu cầu đến API /employees/getall")
            response = requests.get(api_url, headers=headers)
            print(f"Token sau khi gọi API: {access_token}")
            if response.status_code == 200:
                self.employees = response.json()
                print("Đã tải danh sách nhân viên từ API!")
            else:
                error_message = response.json().get("detail", f"Không thể tải danh sách nhân viên: {response.status_code}")
                print(f"Lỗi khi tải danh sách nhân viên: {error_message}")
                if response.status_code in (401, 403) and self.stacked_widget:
                    self.logout_signal.emit()
                self.employees = []
        except requests.RequestException as e:
            print(f"Lỗi kết nối đến API /employees/getall: {str(e)}")
            self.employees = []
        except ValueError as e:
            print(f"Lỗi parse JSON từ API /employees/getall: {str(e)}")
            self.employees = []
        except Exception as e:
            print(f"Lỗi không xác định trong load_employees_from_api: {str(e)}")
            self.employees = []
        finally:
            try:
                self.employee_list_ui.populate_employee_list(self.employees)
                print("Hoàn tất load_employees_from_api")
            except Exception as e:
                print(f"Lỗi khi populate_employee_list: {str(e)}")

    def load_image_for_update(self):
        try:
            file_name, _ = QFileDialog.getOpenFileName(
                None, "Chọn ảnh", "", "Image Files (*.png *.jpg *.jpeg *.bmp)"
            )
            if file_name:
                pixmap = QPixmap(file_name)
                if pixmap.isNull():
                    self.employee_detail_ui.photoLabel.setText("No Image")
                    self.employee_detail_ui.selected_image_path = None
                    return
                scaled_pixmap = pixmap.scaled(140, 168, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                self.employee_detail_ui.photoLabel.setPixmap(scaled_pixmap)
                self.employee_detail_ui.photoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.employee_detail_ui.selected_image_path = file_name
            else:
                self.employee_detail_ui.selected_image_path = None
        except Exception as e:
            print(f"Lỗi khi chọn ảnh: {str(e)}")
            self.employee_detail_ui.selected_image_path = None

    def add_new_employee_safe(self):
        try:
            add_new_employee(self, self.mtcnn, self.facenet)
            self.load_employees_from_api()
        except Exception as e:
            print(f"Lỗi khi thêm nhân viên: {str(e)}")
            
    def displayEmployeeDetails(self, item):
        try:
            emp = item.data(QtCore.Qt.ItemDataRole.UserRole)
            if not emp:
                return

            self.employee_detail_ui.lineEdits["Mã nhân viên:"].setText(emp.get('employee_code', ''))
            self.employee_detail_ui.lineEdits["Họ tên:"].setText(emp.get('full_name', ''))
            self.employee_detail_ui.lineEdits["Chức vụ:"].setText(emp.get('position', ''))
            self.employee_detail_ui.lineEdits["Nơi làm việc:"].setText(emp.get('department', ''))
            self.employee_detail_ui.lineEdits["Email:"].setText(emp.get('email', ''))
            self.employee_detail_ui.lineEdits["Số điện thoại:"].setText(emp.get('phone', ''))

            avatar_url = emp.get('avatar_url')
            self.employee_detail_ui.set_avatar(avatar_url)
            
            self.employee_detail_ui.groupBox.setVisible(True)
        except Exception as e:
            print(f"Lỗi khi hiển thị chi tiết nhân viên: {str(e)}")
            self.employee_detail_ui.groupBox.setVisible(False)

    def toggleEditMode(self):
        try:
            self.isEditing = not getattr(self, 'isEditing', False)
            for key in self.employee_detail_ui.lineEdits:
                if key in ["Mã nhân viên:", "Email:"]:
                    self.employee_detail_ui.lineEdits[key].setReadOnly(True)
                else:
                    self.employee_detail_ui.lineEdits[key].setReadOnly(not self.isEditing)
            
            self.employee_detail_ui.loadImageButton.setVisible(self.isEditing)
            
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
        except Exception as e:
            print(f"Lỗi khi chuyển chế độ chỉnh sửa: {str(e)}")

    def save_employee_changes(self):
        try:
            settings = QSettings("MyApp", "LoginApp")
            access_token = settings.value("access_token")
            print(f"Token trong save_employee_changes: {access_token}")

            if not access_token:
                print("Không tìm thấy access_token trong save_employee_changes")
                if self.stacked_widget:
                    self.logout_signal.emit()
                return

            employee_code = self.employee_detail_ui.lineEdits["Mã nhân viên:"].text()
            if not employee_code:
                return

            update_data = {
                "full_name": self.employee_detail_ui.lineEdits["Họ tên:"].text(),
                "position": self.employee_detail_ui.lineEdits["Chức vụ:"].text(),
                "department": self.employee_detail_ui.lineEdits["Nơi làm việc:"].text(),
                "email": self.employee_detail_ui.lineEdits["Email:"].text(),
                "phone": self.employee_detail_ui.lineEdits["Số điện thoại:"].text(),
            }

            if not update_data["full_name"].strip():
                return

            for key in update_data:
                if update_data[key] is None:
                    update_data[key] = ""

            api_url = f"http://127.0.0.1:8000/employees/update/{employee_code}"
            headers = {"Authorization": f"Bearer {access_token}"}
            files = {}

            if hasattr(self.employee_detail_ui, 'selected_image_path') and self.employee_detail_ui.selected_image_path:
                if not os.path.exists(self.employee_detail_ui.selected_image_path):
                    return
                with open(self.employee_detail_ui.selected_image_path, 'rb') as file_obj:
                    files['file'] = ('avatar.jpg', file_obj, 'image/jpeg')
                    response = requests.put(api_url, data=update_data, files=files, headers=headers)
            else:
                response = requests.put(api_url, data=update_data, headers=headers)

            if response.status_code == 200:
                self.load_employees_from_api()
                self.employee_detail_ui.selected_image_path = None
            else:
                if response.status_code in (401, 403) and self.stacked_widget:
                    self.logout_signal.emit()
        except requests.RequestException as e:
            print(f"Lỗi khi cập nhật nhân viên: {str(e)}")
        except Exception as e:
            print(f"Lỗi không xác định khi cập nhật nhân viên: {str(e)}")

    def delete_employee(self):
        try:
            settings = QSettings("MyApp", "LoginApp")
            access_token = settings.value("access_token")
            print(f"Token trong delete_employee: {access_token}")

            if not access_token:
                print("Không tìm thấy access_token trong delete_employee")
                if self.stacked_widget:
                    self.logout_signal.emit()
                return

            employee_code = self.employee_detail_ui.lineEdits["Mã nhân viên:"].text()
            if not employee_code:
                return

            reply = QMessageBox.question(None, "Xác nhận", f"Bạn có chắc chắn muốn xóa nhân viên {employee_code}?",
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply != QMessageBox.StandardButton.Yes:
                return

            api_url = f"http://127.0.0.1:8000/employees/{employee_code}"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.delete(api_url, headers=headers)
            if response.status_code == 204:
                self.load_employees_from_api()
                for key in self.employee_detail_ui.lineEdits:
                    self.employee_detail_ui.lineEdits[key].clear()
                self.employee_detail_ui.photoLabel.setText("No Image")
                self.employee_detail_ui.selected_image_path = None
                self.employee_detail_ui.groupBox.setVisible(False)
            else:
                if response.status_code in (401, 403) and self.stacked_widget:
                    self.logout_signal.emit()
        except requests.RequestException as e:
            print(f"Lỗi khi xóa nhân viên: {str(e)}")
        except Exception as e:
            print(f"Lỗi không xác định khi xóa nhân viên: {str(e)}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    informationUI = QWidget()
    ui = Ui_informationUI()
    ui.setupUi(informationUI)
    informationUI.show()
    sys.exit(app.exec())