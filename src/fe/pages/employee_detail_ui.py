from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import requests

class EmployeeDetailUI:
    def __init__(self, parent_layout):
        self.groupBox = QGroupBox("Chi tiết nhân viên")
        self.groupBox.setStyleSheet("""
            QGroupBox {
                background-color: #1E2A38;
                border: 2px solid #2E3A4E;
                border-radius: 8px;
                margin-top: 10px;
                font-size: 16px;
                color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 3px;
                color: #A4F9C8;
                font-weight: bold;
            }
        """)
        self.groupBox.setMinimumWidth(400)  # Mở rộng khung "Chi tiết nhân viên"
        self.layout = QVBoxLayout(self.groupBox)
        
        # Photo layout (avatar and "Chọn ảnh" button)
        self.photoLayout = QHBoxLayout()
        
        # Photo label
        self.photoLabel = QLabel("No Image")
        self.photoLabel.setFixedSize(140, 168)
        self.photoLabel.setStyleSheet("border: 1px solid #2E3A4E; border-radius: 5px; color: #C0C0C0;")
        self.photoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.photoLayout.addWidget(self.photoLabel)
        
        # Load Image button (Chọn ảnh)
        self.loadImageButton = QPushButton("Chọn ảnh")
        self.loadImageButton.setFixedSize(100, 30)
        self.loadImageButton.setStyleSheet("""
            QPushButton {
                background-color: #415A77;
                color: white;
                border-radius: 5px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #31445B;
            }
        """)
        self.loadImageButton.setVisible(False)  # Ban đầu ẩn nút "Chọn ảnh"
        self.photoLayout.addWidget(self.loadImageButton)
        
        self.layout.addLayout(self.photoLayout)
        
        # Employee details
        self.detailLayout = QVBoxLayout()
        labels = ["Mã nhân viên:", "Họ tên:", "Chức vụ:", "Nơi làm việc:", "Email:", "Số điện thoại:"]
        self.lineEdits = {}
        
        for label_text in labels:
            rowLayout = QHBoxLayout()
            label = QLabel(label_text)
            label.setStyleSheet("""
                color: #A4F9C8;
                font-size: 16px;
                font-weight: 700;
                text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
                border: none;
                background: none;
            """)
            rowLayout.addWidget(label)
            
            lineEdit = QLineEdit()
            lineEdit.setStyleSheet("""
                background-color: #1E2A38;
                color: white;
                font-size: 14px;
                padding: 6px;
                border-radius: 4px;
                border: 1px solid #5A6986;
                box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
                transition: all 0.3s ease;
            """)
            lineEdit.mousePressEvent = lambda event, le=lineEdit: le.setStyleSheet("""
                background-color: #1E2A38;
                color: white;
                font-size: 14px;
                padding: 6px;
                border-radius: 4px;
                border: 1px solid #68D477;
                box-shadow: 0 3px 9px rgba(104, 212, 119, 0.4);
            """)
            lineEdit.mouseReleaseEvent = lambda event, le=lineEdit: le.setStyleSheet("""
                background-color: #1E2A38;
                color: white;
                font-size: 14px;
                padding: 6px;
                border-radius: 4px;
                border: 1px solid #5A6986;
                box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
                transition: all 0.3s ease;
            """)
            lineEdit.setReadOnly(True)
            lineEdit.setFixedWidth(450)  # Đặt chiều rộng cố định để các ô có độ dài bằng nhau
            rowLayout.addWidget(lineEdit)
            self.lineEdits[label_text] = lineEdit
            self.detailLayout.addLayout(rowLayout)
        
        self.layout.addLayout(self.detailLayout)
        
        # Buttons layout (Edit, Delete)
        self.buttonLayout = QHBoxLayout()
        
        # Edit button
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
        self.buttonLayout.addWidget(self.editButton)
        
        # Delete button
        self.deleteButton = QPushButton("Xóa")
        self.deleteButton.setStyleSheet("""
            QPushButton {
                background-color: #F44336;
                color: white;
                padding: 8px 25px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #D32F2F;
            }
        """)
        self.buttonLayout.addWidget(self.deleteButton)
        
        self.layout.addLayout(self.buttonLayout)
        parent_layout.addWidget(self.groupBox)
        
        # Biến để lưu đường dẫn ảnh được chọn
        self.selected_image_path = None
        
        # Ban đầu ẩn khung "Chi tiết nhân viên"
        self.groupBox.setVisible(False)

    def set_avatar(self, avatar_url):
        """Hiển thị ảnh avatar từ URL"""
        try:
            if avatar_url:
                if not avatar_url.startswith(('http://', 'https://')):
                    avatar_url = f"http://127.0.0.1:8000/{avatar_url}"
                response = requests.get(avatar_url)
                response.raise_for_status()
                image_data = response.content
                pixmap = QPixmap()
                pixmap.loadFromData(image_data)
                scaled_pixmap = pixmap.scaled(140, 168, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                self.photoLabel.setPixmap(scaled_pixmap)
                self.photoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            else:
                self.photoLabel.setText("No Image")
                self.photoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        except Exception as e:
            print(f"Không thể tải ảnh avatar: {str(e)}")
            self.photoLabel.setText("No Image")
            self.photoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)