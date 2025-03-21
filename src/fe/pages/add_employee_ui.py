from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QGroupBox, QLabel, QPushButton, QGridLayout, QLineEdit
from PyQt6.QtCore import Qt, QTimer
import cv2
from pages.utils import update_frame

class AddEmployeeUI:
    def __init__(self, parent_widget, mtcnn):
        self.tab2Layout = QHBoxLayout(parent_widget)
        self.tab2Layout.setContentsMargins(10, 10, 10, 10)
        self.tab2Layout.setSpacing(20)
        
        # Left Layout (Camera)
        self.leftLayout = QVBoxLayout()
        self.leftLayout.setSpacing(12)
        self.leftLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cameraLabel = QLabel()
        self.cameraLabel.setFixedSize(280, 350)
        self.cameraLabel.setStyleSheet("""
            border-radius: 12px;
            border: 3px solid qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #68D477, stop:1 #4CAF50);
            background-color: #11203B;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
        """)
        self.cameraLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Không khởi tạo camera ngay
        self.cap = None
        self.mtcnn = mtcnn  # Lưu mtcnn để dùng trong toggleCamera
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame_with_mtcnn)
        
        self.updateFaceButton = QPushButton("Cập nhật dữ liệu khuôn mặt")
        self.updateFaceButton.setStyleSheet("""
            QPushButton {
                background-color: #68D477;
                color: black;
                padding: 6px 10px;
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
        self.updateFaceButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.updateFaceButton.clicked.connect(self.toggleCamera)
        
        self.leftLayout.addWidget(self.cameraLabel)
        self.leftLayout.addWidget(self.updateFaceButton, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.instructionLabel = QLabel("Vui lòng căn chỉnh khuôn mặt của bạn\nvào giữa và nhìn thẳng vào khung hình")
        self.instructionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instructionLabel.setStyleSheet("""
            color: #A4F9C8;
            font-size: 14px;
            font-weight: 500;
            background-color: #11203B;
            padding: 6px;
            border-radius: 4px;
            border: 1px solid #5A6986;
            box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        """)
        self.instructionLabel.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.instructionLabel.mousePressEvent = lambda event: self.instructionLabel.setStyleSheet("""
            color: #A4F9C8;
            font-size: 14px;
            font-weight: 500;
            background-color: #1E2A38;
            padding: 6px;
            border-radius: 4px;
            border: 1px solid #68D477;
            box-shadow: 0 3px 9px rgba(104, 212, 119, 0.4);
        """)
        self.instructionLabel.mouseReleaseEvent = lambda event: self.instructionLabel.setStyleSheet("""
            color: #A4F9C8;
            font-size: 14px;
            font-weight: 500;
            background-color: #11203B;
            padding: 6px;
            border-radius: 4px;
            border: 1px solid #5A6986;
            box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        """)
        self.leftLayout.addWidget(self.instructionLabel)
        self.tab2Layout.addLayout(self.leftLayout)
        
        # Right Layout (Add Employee Detail)
        self.addEmployeeDetail = QGroupBox()
        self.addEmployeeDetail.setStyleSheet("""
            background-color: #0B121F;
            border: none;
        """)
        self.addDetailLayout = QVBoxLayout(self.addEmployeeDetail)
        
        # Photo + Load Button
        photoLayout = QVBoxLayout()
        self.photoLabel2 = QLabel()
        self.photoLabel2.setFixedSize(140, 168)
        self.photoLabel2.setStyleSheet("""
            border-radius: 6px;
            border: 3px solid qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #68D477, stop:1 #4CAF50);
            background-color: #11203B;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
        """)
        self.photoLabel2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.loadImageButton = QPushButton("Chọn ảnh từ máy")
        self.loadImageButton.setStyleSheet("""
            QPushButton {
                background-color: #68D477;
                color: black;
                padding: 6px 10px;
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
        self.loadImageButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        photoLayout.addWidget(self.photoLabel2)
        photoLayout.addWidget(self.loadImageButton, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.topLayout2 = QHBoxLayout()
        self.topLayout2.addStretch()
        self.topLayout2.addLayout(photoLayout)
        self.topLayout2.addStretch()
        self.addDetailLayout.addLayout(self.topLayout2)
        
        # Info Grid (Tab 2)
        self.infoGrid2 = QGridLayout()
        self.infoGrid2.setSpacing(10)
        # Bỏ trường "Mã nhân viên"
        labels_tab2 = ["Họ tên:", "Chức vụ:", "Nơi làm việc:", "Email:", "Số điện thoại:"]
        self.newLineEdits = {}
        for i, label_text in enumerate(labels_tab2):
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
            self.infoGrid2.addWidget(label, i, 0)
            self.infoGrid2.addWidget(line_edit, i, 1)
            self.newLineEdits[label_text] = line_edit
        self.addDetailLayout.addLayout(self.infoGrid2)
        
        # Save Button
        self.buttonLayout2 = QHBoxLayout()
        self.saveButton2 = QPushButton("Lưu thông tin")
        self.saveButton2.setStyleSheet("""
            QPushButton {
                background-color: #68D477;
                color: black;
                padding: 8px 20px;
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
        self.saveButton2.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.buttonLayout2.addStretch()
        self.buttonLayout2.addWidget(self.saveButton2)
        self.buttonLayout2.addStretch()
        self.addDetailLayout.addLayout(self.buttonLayout2)
        
        self.tab2Layout.addWidget(self.addEmployeeDetail)

        # Thuộc tính để lưu đường dẫn ảnh đã chọn
        self.selected_image_path = None

    def toggleCamera(self):
        if self.cap is None or not self.cap.isOpened():
            # Khởi tạo camera khi nhấn nút
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            if not self.cap.isOpened():
                print("Không thể mở camera. Vui lòng kiểm tra thiết bị hoặc chỉ số camera.")
                self.cameraLabel.setText("Không thể kết nối camera")
                return
            self.timer.start(30)
            self.updateFaceButton.setText("Tắt camera")
            self.updateFaceButton.setStyleSheet("""
                QPushButton {
                    background-color: #FF4D4D;
                    color: white;
                    padding: 6px 10px;
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
        else:
            self.timer.stop()
            if self.cap is not None:
                self.cap.release()  # Giải phóng camera
                self.cap = None
            self.cameraLabel.clear()
            self.updateFaceButton.setText("Cập nhật dữ liệu khuôn mặt")
            self.updateFaceButton.setStyleSheet("""
                QPushButton {
                    background-color: #68D477;
                    color: black;
                    padding: 6px 10px;
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

    def update_frame_with_mtcnn(self):
        if self.cap is not None and self.cap.isOpened():
            update_frame(self, self.mtcnn)