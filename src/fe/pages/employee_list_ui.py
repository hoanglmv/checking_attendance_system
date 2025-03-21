from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QListWidget, QListWidgetItem, QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
import requests
from io import BytesIO

class EmployeeListUI:
    def __init__(self, parent_layout):
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
                min-height: 100px;
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
        """)
        self.employeeList.setMinimumWidth(350)
        parent_layout.addWidget(self.employeeList)

    def add_employee_to_list(self, emp):
        item = QListWidgetItem()
        itemWidget = QWidget()
        layout = QHBoxLayout(itemWidget)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(10)
        
        photoLabel = QLabel()
        photoLabel.setFixedSize(50, 50)
        photoLabel.setStyleSheet("""
            border: 2px solid qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #68D477, stop:1 #4CAF50);
            background-color: #11203B;
            box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
        """)  # Bỏ border-radius để tạo hình vuông
        
        # Tải ảnh từ avatar_url
        avatar_url = emp.get('avatar_url')
        print(f"Avatar URL cho nhân viên {emp.get('full_name', 'Unknown')}: {avatar_url}")
        if avatar_url:
            try:
                # Thêm tiền tố http://127.0.0.1:8000/ nếu avatar_url không phải là URL đầy đủ
                if not avatar_url.startswith(('http://', 'https://')):
                    avatar_url = f"http://127.0.0.1:8000/{avatar_url}"
                print(f"Đang tải ảnh từ: {avatar_url}")  # Thêm log để debug
                response = requests.get(avatar_url)
                response.raise_for_status()  # Kiểm tra lỗi HTTP
                image_data = response.content
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(image_data)
                scaled_pixmap = pixmap.scaled(50, 50, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
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
            f"Nơi làm việc: {emp.get('department', '')}"
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
        info.setMinimumHeight(80)
        
        layout.addWidget(photoLabel)
        layout.addWidget(info)
        layout.addStretch()
        
        item.setSizeHint(itemWidget.sizeHint())
        self.employeeList.addItem(item)
        self.employeeList.setItemWidget(item, itemWidget)
        item.setData(QtCore.Qt.ItemDataRole.UserRole, emp)

    def populate_employee_list(self, employees):
        self.employeeList.clear()
        for emp in employees:
            self.add_employee_to_list(emp)