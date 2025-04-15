import os
import requests
import re
import sys

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QSettings, pyqtSignal, QObject
from PyQt6.QtGui import QCursor, QMovie

# Nếu bạn có import Ui_informationUI thì để nguyên, nếu không có, hãy xóa nó
# from pages.informationUI import Ui_informationUI

class Ui_loginUI(QObject):
    login_success = pyqtSignal()

    def __init__(self):
        super().__init__()

    def setupUi(self, loginUI):
        loginUI.setObjectName("loginUI")
        loginUI.resize(900, 600)  # Thử đặt kích thước lớn hơn một chút
        loginUI.setWindowTitle("Checking Attendance System")

        # ========== Bước 1: Tạo layout chính cho loginUI ========== #
        main_layout = QtWidgets.QVBoxLayout(loginUI)
        main_layout.setContentsMargins(0, 0, 0, 0)  # loại bỏ viền
        main_layout.setSpacing(0)                   # loại bỏ khoảng cách
        loginUI.setLayout(main_layout)

        # ========== Bước 2: Tạo một QWidget "container" dùng QGridLayout ========== #
        container = QtWidgets.QWidget(loginUI)
        grid = QtWidgets.QGridLayout(container)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(0)
        container.setLayout(grid)
        main_layout.addWidget(container)

        # ========== Bước 3: Tạo QLabel để hiển thị QMovie (ảnh GIF) ========== #
        self.bg_label = QtWidgets.QLabel(container)
        self.bg_label.setScaledContents(True)  # Cho phép co giãn toàn bộ ảnh
        # Xây dựng đường dẫn tương đối cho file GIF
        script_dir = os.path.dirname(os.path.abspath(__file__))
        gif_path = os.path.normpath(os.path.join(script_dir, "..", "Image_and_icon", "CSS-Particles.gif"))
        self.movie = QMovie(gif_path)
        self.bg_label.setMovie(self.movie)
        self.movie.start()

        # Thêm bg_label vào grid (vị trí 0,0)
        grid.addWidget(self.bg_label, 0, 0)
        # Đưa bg_label “xuống dưới cùng”, để các widget khác hiển thị phía trên
        self.bg_label.lower()

        # ========== Bước 4: Tạo GroupBox cho giao diện đăng nhập và đặt vào layout ========== #
        self.groupBox_2 = QtWidgets.QGroupBox(container)
        self.groupBox_2.setFixedSize(500, 350)
        self.groupBox_2.setStyleSheet("background-color: #517078; border-radius: 10px;")

        # Thêm groupBox_2 vào đúng vị trí (vẫn ô grid (0,0)), 
        # nhưng canh giữa (AlignCenter) để nó nằm “trên” background.
        grid.addWidget(self.groupBox_2, 0, 0, QtCore.Qt.AlignmentFlag.AlignCenter)

        # ========== Bước 5: Bên trong groupBox_2, ta tạo layout + các widget đăng nhập ========== #
        self.outerLayout = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.outerLayout.addStretch()

        self.centerWidget = QtWidgets.QWidget()
        self.centerWidget.setFixedSize(400, 350)
        self.innerLayout = QtWidgets.QVBoxLayout(self.centerWidget)
        self.outerLayout.addWidget(self.centerWidget)
        self.outerLayout.addStretch()

        self.label = QtWidgets.QLabel("Đăng nhập", self.groupBox_2)
        self.label.setStyleSheet("color: white; font: bold 20pt 'Times New Roman';")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.innerLayout.addWidget(self.label)

        fields = ["email", "password"]
        placeholders = ["Email", "Mật khẩu"]
        self.inputs = {}

        for field, placeholder in zip(fields, placeholders):
            line_edit = QtWidgets.QLineEdit(self.groupBox_2)
            line_edit.setPlaceholderText(placeholder)
            line_edit.setFixedHeight(45)
            line_edit.setStyleSheet(self.input_style())
            if "password" in field:
                line_edit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
            self.inputs[field] = line_edit
            self.innerLayout.addWidget(line_edit)

        self.login_button = QtWidgets.QPushButton("Đăng nhập", self.groupBox_2)
        self.login_button.setFixedSize(250, 40)
        self.login_button.setStyleSheet(self.get_button_style())
        self.login_button.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.login_button.setDefault(True)  # Cho phép nhấn Enter để đăng nhập
        self.innerLayout.addWidget(self.login_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        # ========== Khu vực các button "Đăng ký" và "Quên mật khẩu" ========== #
        self.actionLayout = QtWidgets.QHBoxLayout()
        self.register_button = QtWidgets.QPushButton("Đăng ký", self.groupBox_2)
        self.register_button.setStyleSheet(self.get_action_button_style())
        self.register_button.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.register_button.clicked.connect(self.open_register)

        self.forgot_button = QtWidgets.QPushButton("Quên mật khẩu", self.groupBox_2)
        self.forgot_button.setStyleSheet(self.get_action_button_style())
        self.forgot_button.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.forgot_button.clicked.connect(self.open_forgot_password)

        self.actionLayout.addWidget(self.register_button)
        self.actionLayout.addWidget(self.forgot_button)
        self.innerLayout.addLayout(self.actionLayout)

        # ========== Label báo lỗi hoặc thành công ========== #
        self.error_label = QtWidgets.QLabel("", self.groupBox_2)
        self.error_label.setStyleSheet("color: red; font-size: 12pt;")
        self.error_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.innerLayout.addWidget(self.error_label)

        self.login_button.clicked.connect(self.validate_login_form)

    # ------------------------------------------------------------------------------
    # Các hàm style
    # ------------------------------------------------------------------------------
    def input_style(self):
        return """
            border: 2px solid white;
            border-radius: 5px;
            color: white;
            font-size: 14px;
            padding: 5px;
            background-color: transparent;
        """

    def get_button_style(self):
        return """
            QPushButton {
                border: 2px solid white;
                color: white;
                font: bold 12pt 'Times New Roman';
                border-radius: 5px;
                background-color: #415A77;
                padding: 5px;
                margin: 0px 20px;
            }
            QPushButton:hover {
                background-color: #31445B;
                border: 2px solid #9FEF00;
            }
        """

    def get_action_button_style(self):
        return """
            QPushButton {
                color: white;
                font-size: 10pt;
                background: transparent;
                border: none;
            }
            QPushButton:hover {
                text-decoration: underline;
                color: #9FEF00;
            }
        """

    # ------------------------------------------------------------------------------
    # Các hàm logic
    # ------------------------------------------------------------------------------
    def validate_login_form(self):
        email = self.inputs["email"].text().strip()
        password = self.inputs["password"].text().strip()
        if not email or not password:
            self.show_error("Cần phải điền đầy đủ thông tin!")
            return
        if not self.validate_email(email):
            self.show_error("Email không hợp lệ!")
            return
        self.error_label.setText("")
        self.process_login(email, password)

    def validate_email(self, email):
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(email_regex, email) is not None

    def show_error(self, message):
        self.error_label.setText(message)
        self.error_label.setStyleSheet("color: red; font-size: 12pt;")

    def show_success(self, message):
        self.error_label.setText(message)
        self.error_label.setStyleSheet("color: green; font-size: 12pt;")

    def process_login(self, email, password):
        print(f"Bắt đầu đăng nhập với email: {email}")
        api_url = "http://127.0.0.1:8000/auth/login"
        login_data = {"email": email, "password": password}
        try:
            response = requests.post(api_url, json=login_data)
            response.raise_for_status()
            data = response.json()
            if "access_token" in data:
                settings = QSettings("MyApp", "LoginApp")
                access_token = data["access_token"]
                settings.setValue("access_token", access_token)
                settings.sync()
                self.login_success.emit()
                self.clear_inputs()
            else:
                self.show_error(data.get("detail", "Đăng nhập thất bại! Kiểm tra lại thông tin."))
        except requests.RequestException as e:
            if hasattr(e, 'response') and e.response is not None:
                self.show_error(e.response.json().get("detail", str(e)))
            else:
                self.show_error("Không thể kết nối đến máy chủ! Kiểm tra xem backend có đang chạy không.")
        except Exception as e:
            self.show_error(f"Lỗi không xác định: {str(e)}")

    def clear_inputs(self):
        for field in self.inputs:
            self.inputs[field].clear()
        self.error_label.setText("")

    def get_main_window(self):
        widget = self.groupBox_2
        while widget.parent():
            widget = widget.parent()
        return widget

    def open_register(self):
        main_window = self.get_main_window()
        main_window.stacked_widget.setCurrentWidget(main_window.registerUI)

    def open_forgot_password(self):
        main_window = self.get_main_window()
        main_window.stacked_widget.setCurrentWidget(main_window.forgotPasswordUI.enter_email_ui)

# ------------------------------------------------------------------------------
# Chạy thử
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    loginUI = QtWidgets.QWidget()
    ui = Ui_loginUI()
    ui.setupUi(loginUI)
    loginUI.show()
    sys.exit(app.exec())
