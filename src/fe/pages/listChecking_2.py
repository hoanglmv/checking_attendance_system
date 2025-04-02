import requests
from PyQt6 import QtCore, QtWidgets, QtGui

class ListChecking_2(QtWidgets.QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(0, 200))  # Tăng chiều cao tối thiểu
        self.setMaximumSize(QtCore.QSize(16777215, 200))  # Tăng chiều cao tối đa
        self.setStyleSheet("margin-bottom: 5px;")
        self.setTitle("")

        self.employeeLayout = QtWidgets.QVBoxLayout(self)
        self.employeeLayout.setContentsMargins(5, 5, 5, 5)
        self.employeeLayout.setSpacing(5)

        # Department filter
        self.department_filter = QtWidgets.QComboBox(self)
        self.department_filter.setMinimumWidth(150)
        self.department_filter.setMaximumWidth(200)
        self.department_filter.setStyleSheet("""
            QComboBox {
                background-color: #1E2A38;
                color: white;
                font: 10pt "Times New Roman";
                padding: 6px;
                border: 2px solid #5A6986;
                border-radius: 5px;
            }
            QComboBox:hover {
                border: 2px solid #68D477;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: url(src/fe/Image_and_icon/down-arrow.png);
                width: 12px;
                height: 12px;
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
        self.department_filter.addItem("Tất cả phòng ban")
        self.department_filter.currentTextChanged.connect(self.filter_by_department)

        filter_widget = QtWidgets.QWidget()
        filter_layout = QtWidgets.QHBoxLayout(filter_widget)
        filter_layout.setContentsMargins(5, 0, 5, 0)
        filter_layout.addWidget(self.department_filter)
        filter_layout.addStretch()
        self.employeeLayout.addWidget(filter_widget)

        # Employee list
        self.employeeList = QtWidgets.QListWidget(self)
        self.employeeList.setStyleSheet("""
            QListWidget {
                background-color: #0B121F;
                border-top: 2px solid white;
                padding-bottom: 10px;  /* Thêm padding để dành chỗ cho thanh trượt ngang */
            }
            QListWidget::item {
                background-color: #192E44;
                border: 1px solid #5A6986;
                border-radius: 8px;
                padding: 5px;
                margin: 5px 5px 5px 5px;  /* Điều chỉnh margin để không che thanh trượt */
                color: white;
            }
            QListWidget::item:selected {
                border: 2px solid #9FEF00;
                background-color: #0F2A47;
            }
            QListWidget::horizontalScrollBar {
                background: #0B121F;
                height: 8px;
                margin: 0px;
                border-radius: 4px;
            }
            QListWidget::horizontalScrollBar::handle {
                background: #68D477;
                border-radius: 4px;
                min-width: 20px;
                transition: background 0.3s ease;  /* Thêm hiệu ứng mượt mà */
            }
            QListWidget::horizontalScrollBar::handle:hover {
                background: #5AC469;
            }
            QListWidget::horizontalScrollBar::add-line, QListWidget::horizontalScrollBar::sub-line {
                background: none;
                width: 0px;
            }
            QListWidget::horizontalScrollBar::add-page, QListWidget::horizontalScrollBar::sub-page {
                background: none;
            }
            QListWidget::verticalScrollBar {
                background: none;
                width: 0px;
            }
        """)
        self.employeeList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.employeeList.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.employeeList.setViewMode(QtWidgets.QListView.ViewMode.IconMode)
        self.employeeList.setFlow(QtWidgets.QListView.Flow.LeftToRight)
        self.employeeList.setWrapping(False)
        self.employeeList.setFixedHeight(170)  # Tăng chiều cao của danh sách
        self.employeeList.setSpacing(10)
        self.employeeLayout.addWidget(self.employeeList)

    def load_employees(self):
        print("Bắt đầu load_employees")
        url = "http://127.0.0.1:8000/employees/getall"
        try:
            settings = QtCore.QSettings("MyApp", "LoginApp")
            access_token = settings.value("access_token")
            if not access_token:
                print("Không có token")
                QtWidgets.QMessageBox.critical(None, "Lỗi", "Không tìm thấy token. Vui lòng đăng nhập lại!")
                return

            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            employees = response.json()

            if not isinstance(employees, list):
                print(f"Dữ liệu không phải danh sách: {employees}")
                QtWidgets.QMessageBox.warning(None, "Cảnh báo", "Dữ liệu nhân viên không hợp lệ!")
                return

            self.all_employees = []
            self.employeeList.clear()
            for emp in employees:
                employee_data = {
                    "id": emp.get("employee_code", ""),
                    "name": emp.get("full_name", ""),
                    "position": emp.get("position", ""),
                    "office": emp.get("department", ""),
                    "employee_id": emp.get("id", ""),
                    "avatar_url": emp.get("avatar_url", "")
                }
                self.all_employees.append(employee_data)

            self.load_departments()
            self.department_filter.setCurrentText("Tất cả phòng ban")
            self.filter_by_department("Tất cả phòng ban")

            # Tự động chọn nhân viên đầu tiên nếu danh sách không rỗng
            if self.employeeList.count() > 0:
                print("Tự động chọn nhân viên đầu tiên")
                self.employeeList.setCurrentRow(0)
                first_item = self.employeeList.item(0)
                if first_item and self.employeeList.receivers(self.employeeList.itemClicked) > 0:  # Kiểm tra kết nối
                    print("Phát tín hiệu itemClicked")
                    self.employeeList.itemClicked.emit(first_item)
                else:
                    print("Chưa có kết nối itemClicked hoặc item không hợp lệ")

            print("Kết thúc load_employees")
        except requests.RequestException as e:
            print(f"Lỗi trong load_employees: {str(e)}")
            QtWidgets.QMessageBox.critical(None, "Lỗi", f"Không thể tải danh sách nhân viên: {str(e)}")
        except Exception as e:
            print(f"Lỗi không mong đợi trong load_employees: {str(e)}")
            QtWidgets.QMessageBox.critical(None, "Lỗi", f"Lỗi không xác định: {str(e)}")

    def load_departments(self):
        url = "http://127.0.0.1:8000/employees/departments"
        try:
            settings = QtCore.QSettings("MyApp", "LoginApp")
            access_token = settings.value("access_token")
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            departments = response.json()

            self.department_filter.clear()
            self.department_filter.addItem("Tất cả phòng ban")
            for dept in departments:
                self.department_filter.addItem(dept)

        except requests.RequestException as e:
            QtWidgets.QMessageBox.critical(None, "Lỗi", f"Không thể tải danh sách phòng ban: {str(e)}")

    def filter_by_department(self, department):
        self.employeeList.clear()
        if department == "Tất cả phòng ban":
            filtered_employees = self.all_employees
        else:
            filtered_employees = [emp for emp in self.all_employees if emp.get('office') == department]

        for emp in filtered_employees:
            self.add_employee_to_list(emp)

    def add_employee_to_list(self, emp):
        item = QtWidgets.QListWidgetItem()
        itemWidget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(itemWidget)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(10)

        # Avatar
        photoLabel = QtWidgets.QLabel()
        photoLabel.setFixedSize(60, 60)
        photoLabel.setStyleSheet("""
            border: 2px solid qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #68D477, stop:1 #4CAF50);
            background-color: #11203B;
            box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
        """)

        avatar_url = emp.get('avatar_url')
        print(f"Avatar URL cho nhân viên {emp.get('name', 'Unknown')}: {avatar_url}")
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
                scaled_pixmap = pixmap.scaled(60, 60, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
                photoLabel.setPixmap(scaled_pixmap)
                photoLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            except Exception as e:
                print(f"Không thể tải ảnh avatar cho nhân viên {emp.get('name', 'Unknown')}: {str(e)}")
                photoLabel.setText("No Image")
                photoLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        else:
            photoLabel.setText("No Image")
            photoLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Thông tin nhân viên
        info_text = (
            f"ID: {emp.get('id', '')}\n"
            f"Họ tên: {emp.get('name', '')}\n"
            f"Chức vụ: {emp.get('position', '')}\n"
            f"Nơi làm việc: {emp.get('office', '')}"
        )
        info = QtWidgets.QLabel(info_text)
        info.setStyleSheet("""
            color: white;
            font-size: 10px;
            font-weight: 500;
            line-height: 1.5;
        """)
        info.setWordWrap(True)
        info.setMinimumWidth(150)
        info.setMinimumHeight(80)

        layout.addWidget(photoLabel)
        layout.addWidget(info)
        layout.addStretch()

        item.setSizeHint(itemWidget.sizeHint())
        self.employeeList.addItem(item)
        self.employeeList.setItemWidget(item, itemWidget)
        item.setData(QtCore.Qt.ItemDataRole.UserRole, emp)