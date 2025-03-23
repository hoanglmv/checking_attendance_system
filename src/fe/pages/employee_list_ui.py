from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QListWidget, QListWidgetItem, QWidget, QHBoxLayout, QLabel, QAbstractItemView, QComboBox, QVBoxLayout
from PyQt6.QtCore import Qt
import requests
from io import BytesIO

class EmployeeListUI:
    def __init__(self, parent_layout):
        # Tạo layout chính để chứa bộ lọc và danh sách nhân viên
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(10)

        # Tạo bộ lọc theo phòng ban
        self.department_filter = QComboBox()
        self.department_filter.setMinimumWidth(200)
        self.department_filter.setMaximumWidth(300)
        self.department_filter.setStyleSheet("""
            QComboBox {
                background-color: #1E2A38;
                color: white;
                font: 12pt "Times New Roman";
                padding: 8px;
                border: 2px solid #5A6986;
                border-radius: 5px;
            }
            QComboBox:hover {
                border: 2px solid #68D477;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: url(src/fe/Image_and_icon/down-arrow.png);
                width: 16px;
                height: 16px;
            }
            QComboBox QAbstractItemView {
                background-color: #1E2A38;
                color: white;
                selection-background-color: #68D477;
                selection-color: black;
                border: 1px solid #5A6986;
                border-radius: 5px;
            }
        """)
        self.department_filter.addItem("Tất cả phòng ban")  # Mặc định hiển thị tất cả
        self.department_filter.currentTextChanged.connect(self.filter_by_department)  # Kết nối sự kiện thay đổi

        # Thêm bộ lọc vào layout (không có nhãn)
        filter_widget = QWidget()
        filter_layout = QHBoxLayout(filter_widget)
        filter_layout.setContentsMargins(0, 0, 0, 0)
        filter_layout.addWidget(self.department_filter)
        filter_layout.addStretch()
        self.main_layout.addWidget(filter_widget)

        # Tạo danh sách nhân viên
        self.employeeList = QListWidget()
        self.employeeList.setStyleSheet("""
            QListWidget {
                background-color: #0B121F;
                border: 1px solid #1E2A38;
                border-radius: 6px;
                padding: 6px;
            }
            QListWidget::item {
                background-color: #11203B;
                border: 1px solid #5A6986;
                border-radius: 4px;
                padding: 8px;
                margin: 4px 0;
                color: white;
                font-size: 12px;
                transition: all 0.3s ease;
                min-height: 130px;
            }
            QListWidget::item:hover {
                background-color: #1E2A38;
                border: 2px solid #68D477;
                transform: scale(1.02);
                box-shadow: 0 3px 9px rgba(104, 212, 119, 0.3);
            }
            QListWidget::item:selected {
                background-color: #0F2A47;
                border: 2px solid #68D477;
                box-shadow: 0 2px 6px rgba(104, 212, 119, 0.3);
            }
            QListWidget::verticalScrollBar {
                background: #0B121F;
                width: 10px;
                margin: 0px;
                border-radius: 5px;
            }
            QListWidget::verticalScrollBar::handle {
                background: #68D477;
                border-radius: 5px;
                min-height: 20px;
            }
            QListWidget::verticalScrollBar::handle:hover {
                background: #5AC469;
            }
            QListWidget::verticalScrollBar::add-line, QListWidget::verticalScrollBar::sub-line {
                background: none;
                height: 0px;
            }
            QListWidget::verticalScrollBar::add-page, QListWidget::verticalScrollBar::sub-page {
                background: none;
            }
        """)
        self.employeeList.setMinimumWidth(350)

        # Đặt chế độ cuộn mượt
        self.employeeList.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.employeeList.verticalScrollBar().setSingleStep(10)

        # Thêm danh sách nhân viên vào layout
        self.main_layout.addWidget(self.employeeList)

        # Thêm layout chính vào parent_layout
        parent_layout.addLayout(self.main_layout)

        # Lưu trữ danh sách nhân viên gốc để lọc
        self.all_employees = []

    def load_departments(self):
        """Tải danh sách phòng ban từ API"""
        try:
            settings = QtCore.QSettings("MyApp", "LoginApp")
            access_token = settings.value("access_token")
            if not access_token:
                print("Không tìm thấy access_token để tải danh sách phòng ban!")
                QtWidgets.QMessageBox.critical(None, "Lỗi", "Không tìm thấy access_token. Vui lòng đăng nhập lại!")
                return

            api_url = "http://127.0.0.1:8000/employees/departments"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()  # Kiểm tra lỗi HTTP
            departments = response.json()
            print(f"Danh sách phòng ban từ API: {departments}")

            if not departments:  # Nếu danh sách rỗng
                print("Không có phòng ban nào trong cơ sở dữ liệu!")
                QtWidgets.QMessageBox.warning(None, "Thông báo", "Không có phòng ban nào trong cơ sở dữ liệu!")
                return

            # Xóa các mục hiện có trong QComboBox và thêm lại
            self.department_filter.clear()
            self.department_filter.addItem("Tất cả phòng ban")
            for dept in departments:
                print(f"Thêm phòng ban vào QComboBox: {dept}")
                self.department_filter.addItem(dept)
            
            # Cập nhật giao diện
            self.department_filter.update()
            print(f"Số lượng mục trong QComboBox: {self.department_filter.count()}")

        except requests.RequestException as e:
            print(f"Không thể tải danh sách phòng ban: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Chi tiết lỗi: {e.response.status_code} - {e.response.text}")
                QtWidgets.QMessageBox.critical(None, "Lỗi", f"Không thể tải danh sách phòng ban: {e.response.status_code} - {e.response.text}")
            else:
                QtWidgets.QMessageBox.critical(None, "Lỗi", f"Không thể kết nối đến API: {str(e)}")

    def filter_by_department(self, department):
        """Lọc danh sách nhân viên theo phòng ban"""
        try:
            print(f"Lọc danh sách nhân viên theo phòng ban: {department}")
            if not self.all_employees:
                print("Danh sách nhân viên rỗng, không thể lọc!")
                return

            self.employeeList.clear()
            if department == "Tất cả phòng ban":
                filtered_employees = self.all_employees
            else:
                filtered_employees = [emp for emp in self.all_employees if emp.get('department') == department]

            print(f"Số lượng nhân viên sau khi lọc: {len(filtered_employees)}")
            for emp in filtered_employees:
                self.add_employee_to_list(emp)

        except Exception as e:
            print(f"Lỗi khi lọc danh sách nhân viên: {str(e)}")

    def add_employee_to_list(self, emp):
        try:
            item = QListWidgetItem()
            itemWidget = QWidget()
            layout = QHBoxLayout(itemWidget)
            layout.setContentsMargins(6, 6, 6, 6)
            layout.setSpacing(10)
            
            photoLabel = QLabel()
            photoLabel.setFixedSize(80, 80)
            photoLabel.setStyleSheet("""
                border: 2px solid qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #68D477, stop:1 #4CAF50);
                background-color: #11203B;
                box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
            """)
            
            avatar_url = emp.get('avatar_url')
            print(f"Avatar URL cho nhân viên {emp.get('full_name', 'Unknown')}: {avatar_url}")
            if avatar_url:
                try:
                    if not avatar_url.startswith(('http://', 'https://')):
                        avatar_url = f"http://127.0.0.1:8000/{avatar_url}"
                    print(f"Đang tải ảnh từ: {avatar_url}")
                    response = requests.get(avatar_url)
                    response.raise_for_status()
                    image_data = response.content
                    pixmap = QtGui.QPixmap()
                    pixmap.loadFromData(image_data)
                    scaled_pixmap = pixmap.scaled(80, 80, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
                    photoLabel.setPixmap(scaled_pixmap)
                    photoLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                except Exception as e:
                    print(f"Không thể tải ảnh avatar cho nhân viên {emp.get('full_name', 'Unknown')}: {str(e)}")
                    photoLabel.setText("No Image")
                    photoLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            else:
                photoLabel.setText("No Image")
                photoLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            info_text = (
                f"Mã nhân viên: {emp.get('employee_code', '')}\n"
                f"Họ tên: {emp.get('full_name', '')}\n"
                f"Chức vụ: {emp.get('position', '')}\n"
                f"Phòng ban: {emp.get('department', '')}"
            )
            info = QLabel(info_text)
            info.setStyleSheet("""
                color: white;
                font-size: 12px;
                font-weight: 500;
                line-height: 1.5;
            """)
            info.setWordWrap(True)
            info.setMinimumWidth(250)
            info.setMinimumHeight(110)
            info.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
            
            layout.addWidget(photoLabel)
            layout.addWidget(info)
            layout.addStretch()
            
            item.setSizeHint(itemWidget.sizeHint())
            self.employeeList.addItem(item)
            self.employeeList.setItemWidget(item, itemWidget)
            item.setData(QtCore.Qt.ItemDataRole.UserRole, emp)

        except Exception as e:
            print(f"Lỗi khi thêm nhân viên vào danh sách: {str(e)}")

    def populate_employee_list(self, employees):
        try:
            print(f"Đang tải danh sách nhân viên, số lượng: {len(employees)}")
            print(f"Danh sách nhân viên: {employees}")

            # Làm sạch danh sách trước khi thêm mới
            self.all_employees = []
            self.employeeList.clear()

            # Lưu trữ danh sách nhân viên gốc
            self.all_employees = employees

            # Ngắt kết nối sự kiện currentTextChanged để tránh gọi filter_by_department không mong muốn
            self.department_filter.currentTextChanged.disconnect()
            
            # Tải danh sách phòng ban
            self.load_departments()

            # Đặt lại bộ lọc về mặc định
            self.department_filter.setCurrentText("Tất cả phòng ban")

            # Kết nối lại sự kiện currentTextChanged
            self.department_filter.currentTextChanged.connect(self.filter_by_department)

            # Hiển thị danh sách nhân viên
            for emp in employees:
                self.add_employee_to_list(emp)

            print(f"Số lượng nhân viên trong danh sách: {self.employeeList.count()}")

        except Exception as e:
            print(f"Lỗi khi tải danh sách nhân viên: {str(e)}")