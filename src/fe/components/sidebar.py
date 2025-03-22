from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QGroupBox, QPushButton, QLabel, QVBoxLayout, QGridLayout, QSpacerItem, QSizePolicy, QMessageBox
from PyQt6.QtCore import QSettings, pyqtSignal
from PyQt6.QtGui import QCursor, QIcon
import requests

class Sidebar(QGroupBox):
    logout_signal = pyqtSignal()  # Tín hiệu để thông báo đăng xuất

    def __init__(self, parent=None, stacked_widget=None):
        super().__init__(parent)

        # Lưu tham chiếu đến stacked_widget để chuyển đổi giao diện
        self.stacked_widget = stacked_widget

        self.setMinimumSize(QtCore.QSize(280, 0))
        self.setMaximumSize(QtCore.QSize(280, 16777215))
        self.setStyleSheet("background-color: #122131;")

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(35, 0, 35, 0)
        self.verticalLayout.setSpacing(20) 

        # Logo
        self.logo = QLabel(self)
        self.logo.setMinimumSize(QtCore.QSize(200, 180))
        self.logo.setMaximumSize(QtCore.QSize(200, 180))
        self.logo.setStyleSheet("""
            background-image: url(src/fe/Image_and_icon/logo.png);
            background-repeat: no-repeat;
            background-position: center center;
            background-size: contain;
        """)
        self.verticalLayout.addWidget(self.logo)

        # Button: Attendance
        self.fil_attendance = self.create_button_container()
        self.btn_attendance = self.create_button(
            "src/fe/Image_and_icon/icons8-user-30.png",
            "Điểm danh"
        )
        self.fil_attendance.layout().addWidget(self.btn_attendance)
        self.verticalLayout.addWidget(self.fil_attendance)

        # Button: Manage
        self.fil_manage = self.create_button_container()
        self.btn_manage = self.create_button(
            "src/fe/Image_and_icon/icons8-user-30.png",
            "Quản lý"
        )
        self.fil_manage.layout().addWidget(self.btn_manage)
        self.verticalLayout.addWidget(self.fil_manage)

        # Spacer
        spacer = QSpacerItem(20, 300, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacer)

        # Button: Logout
        self.fil_logout = self.create_button_container()
        self.btn_logout = self.create_button(
            "src/fe/Image_and_icon/icons8-logout-30.png",
            "Đăng xuất"
        )
        # Tùy chỉnh style cho nút Đăng xuất để cân xứng hơn
        self.btn_logout.setStyleSheet("""
            QPushButton {
                background-image: url(src/fe/Image_and_icon/icons8-logout-30.png);
                background-repeat: no-repeat;
                background-position: left center;
                background-size: 24px 24px;
                color: white;
                font: 12pt "Times New Roman";
                padding-left: 20px;
                padding-right: 20px;  /* Thêm padding bên phải để cân đối */
                border: 2px solid white;
                border-radius: 5px;
                background-color: #F44336;
                text-align: center;  /* Căn giữa chữ */
            }
            QPushButton:hover {
                background-color: #D32F2F;
                border: 2px solid #FFD700;
            }
        """)
        self.btn_logout.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_logout.clicked.connect(self.logout)
        self.fil_logout.layout().addWidget(self.btn_logout)
        self.verticalLayout.addWidget(self.fil_logout)

    def create_button_container(self):
        container = QGroupBox(self)
        container.setMinimumSize(QtCore.QSize(200, 58))
        container.setMaximumSize(QtCore.QSize(200, 58))
        layout = QGridLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        return container

    def create_button(self, icon_path, text):
        button = QPushButton(self)
        button.setMinimumSize(QtCore.QSize(180, 32))
        button.setMaximumSize(QtCore.QSize(180, 32))
        button.setText(text)
        button.setStyleSheet(f"""
            background-image: url({icon_path});
            background-repeat: no-repeat;
            background-position: left center;
            background-size: 24px 24px;
            color: white;
            font: 12pt "Times New Roman";
            padding-left: 40px;
        """)
        return button

    def logout(self):
        """Xử lý đăng xuất: Gọi API logout và phát tín hiệu để quay lại loginUI"""
        print("Bắt đầu đăng xuất từ Sidebar")
        settings = QSettings("MyApp", "LoginApp")
        access_token = settings.value("access_token")

        if not access_token:
            print("Không tìm thấy access_token, không cần gọi API logout")
            QMessageBox.warning(None, "Thông báo", "Bạn chưa đăng nhập!")
            return

        # Tạo thông báo xác nhận với giao diện tùy chỉnh
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Xác nhận đăng xuất")
        msg_box.setText("Bạn có chắc chắn muốn đăng xuất không?")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg_box.setDefaultButton(QMessageBox.StandardButton.No)

        # Tùy chỉnh giao diện của QMessageBox
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #1E2A38;
                color: white;
                font: 14pt "Times New Roman";
            }
            QMessageBox QLabel {
                color: white;
            }
            QMessageBox QPushButton {
                background-color: #68D477;
                color: black;
                padding: 8px 16px;
                border-radius: 5px;
                font: 12pt "Times New Roman";
                border: 1px solid #68D477;
            }
            QMessageBox QPushButton:hover {
                background-color: #5AC469;
                border: 1px solid #5AC469;
            }
            QMessageBox QPushButton:pressed {
                background-color: #4CAF50;
            }
        """)

        # Tùy chỉnh nút Yes và No
        yes_button = msg_box.button(QMessageBox.StandardButton.Yes)
        yes_button.setText("Có")
        yes_button.setStyleSheet("""
            QPushButton {
                background-color: #F44336;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
                font: 12pt "Times New Roman";
                border: 1px solid #F44336;
            }
            QPushButton:hover {
                background-color: #D32F2F;
                border: 1px solid #FFD700;
            }
            QPushButton:pressed {
                background-color: #C62828;
            }
        """)

        no_button = msg_box.button(QMessageBox.StandardButton.No)
        no_button.setText("Không")
        no_button.setStyleSheet("""
            QPushButton {
                background-color: #68D477;
                color: black;
                padding: 8px 16px;
                border-radius: 5px;
                font: 12pt "Times New Roman";
                border: 1px solid #68D477;
            }
            QPushButton:hover {
                background-color: #5AC469;
                border: 1px solid #5AC469;
            }
            QPushButton:pressed {
                background-color: #4CAF50;
            }
        """)

        # Thêm biểu tượng (icon) cho thông báo
        msg_box.setIcon(QMessageBox.Icon.Question)

        # Hiển thị thông báo và xử lý kết quả
        reply = msg_box.exec()
        if reply != QMessageBox.StandardButton.Yes:
            print("Người dùng hủy đăng xuất")
            return

        try:
            # Gọi API logout
            api_url = "http://127.0.0.1:8000/auth/logout"
            headers = {"Authorization": f"Bearer {access_token}"}
            print("Gửi yêu cầu đến API /auth/logout")
            response = requests.post(api_url, headers=headers)
            response.raise_for_status()
            print("Đăng xuất thành công qua API")

            # Xóa access_token khỏi QSettings
            settings.remove("access_token")
            print("Đã xóa access_token")

            # Phát tín hiệu để MainWindow xử lý chuyển giao diện
            self.logout_signal.emit()
            print("Đã phát tín hiệu đăng xuất")

        except requests.RequestException as e:
            print(f"Lỗi khi gọi API /auth/logout: {str(e)}")
            error_msg = QMessageBox()
            error_msg.setWindowTitle("Lỗi")
            error_msg.setText(f"Không thể đăng xuất: {str(e)}")
            error_msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            error_msg.setStyleSheet("""
                QMessageBox {
                    background-color: #1E2A38;
                    color: white;
                    font: 14pt "Times New Roman";
                }
                QMessageBox QLabel {
                    color: white;
                }
                QMessageBox QPushButton {
                    background-color: #F44336;
                    color: white;
                    padding: 8px 16px;
                    border-radius: 5px;
                    font: 12pt "Times New Roman";
                    border: 1px solid #F44336;
                }
                QMessageBox QPushButton:hover {
                    background-color: #D32F2F;
                    border: 1px solid #FFD700;
                }
                QMessageBox QPushButton:pressed {
                    background-color: #C62828;
                }
            """)
            error_msg.setIcon(QMessageBox.Icon.Critical)
            error_msg.exec()