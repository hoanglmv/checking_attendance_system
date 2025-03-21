from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QLineEdit, QPushButton
from PyQt6.QtCore import Qt
import requests
from io import BytesIO

class EmployeeDetailUI:
    def __init__(self, parent_layout):
        self.employeeDetail = QGroupBox()
        self.employeeDetail.setStyleSheet("""
            background-color: #0B121F;
            border: none;
        """)
        self.detailLayout = QVBoxLayout(self.employeeDetail)
        self.detailLayout.setSpacing(12)
        
        # Top Layout (Photo + Stats)
        self.topLayout = QHBoxLayout()
        self.topLayout.setSpacing(20)
        self.photoLabel = QLabel()
        self.photoLabel.setFixedSize(180, 216)
        self.photoLabel.setStyleSheet("""
            border-radius: 6px;
            border: 3px solid qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #68D477, stop:1 #4CAF50);
            background-color: #11203B;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
        """)
        self.photoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.statsLayout = QVBoxLayout()
        self.attendanceStats = QLabel("Chuyên cần: ??\nĐến muộn: ??\nVề sớm: ??")
        self.attendanceStats.setStyleSheet("""
            color: #A4F9C8;
            font-size: 14px;
            font-weight: 500;
            background-color: #11203B;
            padding: 8px;
            border-radius: 4px;
            border: 1px solid #5A6986;
            box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        """)
        self.attendanceStats.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.attendanceStats.mousePressEvent = lambda event: self.attendanceStats.setStyleSheet("""
            color: #A4F9C8;
            font-size: 14px;
            font-weight: 500;
            background-color: #1E2A38;
            padding: 8px;
            border-radius: 4px;
            border: 1px solid #68D477;
            box-shadow: 0 3px 9px rgba(104, 212, 119, 0.4);
        """)
        self.attendanceStats.mouseReleaseEvent = lambda event: self.attendanceStats.setStyleSheet("""
            color: #A4F9C8;
            font-size: 14px;
            font-weight: 500;
            background-color: #11203B;
            padding: 8px;
            border-radius: 4px;
            border: 1px solid #5A6986;
            box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        """)
        self.statsLayout.addWidget(self.attendanceStats, alignment=Qt.AlignmentFlag.AlignCenter)
        self.statsLayout.addStretch()
        
        self.topLayout.addStretch()
        self.topLayout.addWidget(self.photoLabel)
        self.topLayout.addLayout(self.statsLayout)
        self.topLayout.addStretch()
        self.detailLayout.addLayout(self.topLayout)
        
        # Info Grid (Tab 1)
        self.infoGrid = QGridLayout()
        self.infoGrid.setSpacing(10)
        self.infoGrid.setColumnStretch(1, 1)
        labels = ["Mã nhân viên:", "Họ tên:", "Chức vụ:", "Nơi làm việc:", "Email:", "Số điện thoại:"]
        self.lineEdits = {}
        for i, label_text in enumerate(labels):
            label = QLabel(label_text)
            label.setStyleSheet("""
                color: #A4F9C8;
                font-size: 16px;
                font-weight: 700;
                text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
                border: none;
                background: none;
            """)
            line_edit = QLineEdit()
            line_edit.setStyleSheet("""
                background-color: #1E2A38;
                color: white;
                font-size: 14px;
                padding: 6px;
                border-radius: 4px;
                border: 1px solid #5A6986;
                box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
                transition: all 0.3s ease;
            """)
            line_edit.setReadOnly(True)
            line_edit.setMinimumWidth(250)
            line_edit.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.IBeamCursor))
            line_edit.mouseMoveEvent = lambda event, le=line_edit: le.setStyleSheet("""
                background-color: #1E2A38;
                color: white;
                font-size: 14px;
                padding: 6px;
                border-radius: 4px;
                border: 1px solid #68D477;
                box-shadow: 0 3px 9px rgba(104, 212, 119, 0.4);
            """)
            line_edit.mousePressEvent = lambda event, le=line_edit: le.setStyleSheet("""
                background-color: #1E2A38;
                color: white;
                font-size: 14px;
                padding: 6px;
                border-radius: 4px;
                border: 1px solid #68D477;
                box-shadow: 0 3px 9px rgba(104, 212, 119, 0.4);
            """)
            line_edit.mouseReleaseEvent = lambda event, le=line_edit: le.setStyleSheet("""
                background-color: #1E2A38;
                color: white;
                font-size: 14px;
                padding: 6px;
                border-radius: 4px;
                border: 1px solid #5A6986;
                box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
                transition: all 0.3s ease;
            """)
            self.infoGrid.addWidget(label, i, 0)
            self.infoGrid.addWidget(line_edit, i, 1)
            self.lineEdits[label_text] = line_edit

        self.detailLayout.addLayout(self.infoGrid)
        self.detailLayout.addStretch()
        
        # Buttons
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setSpacing(20)
        self.deleteButton = QPushButton("Xóa nhân viên")
        self.deleteButton.setStyleSheet("""
            QPushButton {
                background-color: #FF4D4D;
                color: white;
                padding: 8px 25px;
                border-radius: 4px;
                font-size: 14px;
                font-weight: 600;
                border: 1px solid #FF4D4D;
                box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
                transition: all 0.3s ease;
            }
            QPushButton:hover {
                background-color: #CC0000;
                border: 1px solid #CC0000;
                box-shadow: 0 3px 9px rgba(255, 77, 77, 0.4);
                transform: scale(1.05);
            }
        """)
        self.deleteButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.editButton = QPushButton("Thay đổi thông tin")
        self.editButton.setStyleSheet("""
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
        self.editButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.buttonLayout.addStretch()
        self.buttonLayout.addWidget(self.deleteButton)
        self.buttonLayout.addWidget(self.editButton)
        self.buttonLayout.addStretch()
        self.detailLayout.addLayout(self.buttonLayout)
        
        parent_layout.addWidget(self.employeeDetail)

    def set_avatar(self, avatar_url):
        """Hàm để đặt ảnh avatar vào ô vuông"""
        if avatar_url:
            try:
                # Thêm tiền tố http://127.0.0.1:8000/ nếu avatar_url không phải là URL đầy đủ
                if not avatar_url.startswith(('http://', 'https://')):
                    avatar_url = f"http://127.0.0.1:8000/{avatar_url}"
                print(f"Đang tải ảnh avatar từ: {avatar_url}")  # Thêm log để debug
                response = requests.get(avatar_url)
                response.raise_for_status()  # Kiểm tra lỗi HTTP
                image_data = response.content
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(image_data)
                
                # Scale ảnh để vừa ô vuông
                scaled_pixmap = pixmap.scaled(180, 216, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
                self.photoLabel.setPixmap(scaled_pixmap)
                self.photoLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            except Exception as e:
                print(f"Không thể tải ảnh avatar: {str(e)}")
                self.photoLabel.setText("No Image")
                self.photoLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        else:
            self.photoLabel.setText("No Image")
            self.photoLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)