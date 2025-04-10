import os
import subprocess
import requests
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QGroupBox, QPushButton, QLabel, QVBoxLayout, QGridLayout, QSpacerItem, QSizePolicy, QMessageBox
from PyQt6.QtCore import QSettings, pyqtSignal, QSize, Qt
from PyQt6.QtGui import QCursor, QIcon

def get_project_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

class Sidebar(QGroupBox):
    logout_signal = pyqtSignal()       # Signal for logout
    attendance_signal = pyqtSignal()   # Signal for "Attendance" button
    manage_signal = pyqtSignal()       # Signal for "Manage" button

    def __init__(self, parent=None, stacked_widget=None):
        super().__init__(parent)

        self.stacked_widget = stacked_widget
        self.setMinimumSize(QtCore.QSize(280, 0))
        self.setMaximumSize(QtCore.QSize(280, 16777215))
        self.setStyleSheet("""
            QGroupBox {
                background-color: #1B2B40;
                border: none;
                border-radius: 10px;
            }
        """)

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout.setSpacing(15)

        # Logo
        self.logo = QLabel(self)
        self.logo.setMinimumSize(QtCore.QSize(200, 180))
        self.logo.setMaximumSize(QtCore.QSize(200, 180))
        # Lấy đường dẫn tuyệt đối cho logo, từ file hiện tại (components)
        logo_base = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.normpath(os.path.join(logo_base, "..", "Image_and_icon", "logo.png")).replace("\\", "/")
        self.logo.setStyleSheet(f"""
            QLabel {{
                background-image: url({logo_path});
                background-repeat: no-repeat;
                background-position: center;
                border: none;
            }}
        """)
        self.verticalLayout.addWidget(self.logo, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        # Button: Attendance
        self.fil_attendance = self.create_button_container()
        self.btn_attendance = self.create_button("icons8-checking-30.png", "  Điểm danh")
        self.fil_attendance.layout().addWidget(self.btn_attendance)
        self.btn_attendance.clicked.connect(self.attendance_signal.emit)
        self.verticalLayout.addWidget(self.fil_attendance)

        # Button: Manage
        self.fil_manage = self.create_button_container()
        self.btn_manage = self.create_button("icons8-management-30.png", "  Quản lý")
        self.fil_manage.layout().addWidget(self.btn_manage)
        self.btn_manage.clicked.connect(self.manage_signal.emit)
        self.verticalLayout.addWidget(self.fil_manage)

        # Spacer
        spacer = QSpacerItem(20, 300, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacer)

        # Button: Logout
        self.fil_logout = self.create_button_container()
        self.btn_logout = self.create_button("icons8-logout-30.png", "  Đăng xuất")
        self.btn_logout.setStyleSheet("""
            QPushButton {
                border: none;
                border-radius: 5px;
                color: white;
                font: 15pt "Times New Roman";
                padding: 8px 16px 8px 32px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """)
        self.btn_logout.clicked.connect(self.logout)
        self.fil_logout.layout().addWidget(self.btn_logout)
        self.verticalLayout.addWidget(self.fil_logout)

    def create_button_container(self):
        container = QGroupBox(self)
        container.setMinimumSize(QtCore.QSize(200, 58))
        container.setMaximumSize(QtCore.QSize(200, 58))
        container.setStyleSheet("""
            QGroupBox {
                background-color: #1B2B40;
                border: none;
                border-radius: 5px;
            }
        """)
        layout = QGridLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        return container

    def create_button(self, relative_icon_name, text):
        button = QPushButton(text, self)
        button.setMinimumSize(QSize(180, 40))
        button.setMaximumSize(QSize(180, 40))

        # Lấy đường dẫn của file hiện tại (components)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # Từ folder components, lùi 1 cấp để vào src/fe rồi đến folder Image_and_icon
        icon_path = os.path.normpath(os.path.join(base_dir, "..", "Image_and_icon", relative_icon_name))
        if not os.path.exists(icon_path):
            print("❌ Không tìm thấy icon:", icon_path)
        else:
            print("✅ Icon tìm thấy:", icon_path)

        icon = QIcon(icon_path)
        button.setIcon(icon)
        button.setIconSize(QSize(24, 24))

        # Style cho button
        button.setStyleSheet("""
            QPushButton {
                border: none;
                border-radius: 5px;
                color: white;
                font: 15pt "Times New Roman";
                padding: 8px 16px 8px 32px;
                text-align: left;
            }
            QPushButton:hover {
            }
        """)
        button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        return button

    def logout(self):
        settings = QSettings("MyApp", "LoginApp")
        access_token = settings.value("access_token")
        if not access_token:
            QMessageBox.warning(None, "Thông báo", "Bạn chưa đăng nhập!")
            return

        msg_box = QMessageBox()
        msg_box.setWindowTitle("Xác nhận đăng xuất")
        msg_box.setText("Bạn có chắc chắn muốn đăng xuất không?")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg_box.setDefaultButton(QMessageBox.StandardButton.No)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #1E2A38;
                color: white;
                font: 14pt "Arial";
            }
            QMessageBox QLabel {
                color: white;
            }
            QMessageBox QPushButton {
                background-color: #68D477;
                color: black;
                padding: 8px 16px;
                border-radius: 5px;
                font: bold 12pt "Arial";
                border: 1px solid #68D477;
            }
            QMessageBox QPushButton:hover {
                background-color: #5AC469;
            }
            QMessageBox QPushButton:pressed {
                background-color: #4CAF50;
            }
        """)
        reply = msg_box.exec()
        if reply != QMessageBox.StandardButton.Yes:
            return

        try:
            api_url = "http://127.0.0.1:8000/auth/logout"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.post(api_url, headers=headers)
            response.raise_for_status()
            settings.remove("access_token")
            self.logout_signal.emit()
        except requests.RequestException as e:
            error_msg = QMessageBox()
            error_msg.setWindowTitle("Lỗi")
            error_msg.setText(f"Không thể đăng xuất: {str(e)}")
            error_msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            error_msg.setStyleSheet("""
                QMessageBox {
                    background-color: #1E2A38;
                    color: white;
                    font: 14pt "Arial";
                }
                QMessageBox QLabel {
                    color: white;
                }
                QMessageBox QPushButton {
                    color: white;
                    padding: 8px 16px;
                    border-radius: 5px;
                    font: bold 12pt "Arial";
                    border: 1px solid #F44336;
                }
                QMessageBox QPushButton:hover {
                    background-color: #D32F2F;
                }
                QMessageBox QPushButton:pressed {
                    background-color: #C62828;
                }
            """)
            error_msg.setIcon(QMessageBox.Icon.Critical)
            error_msg.exec()
