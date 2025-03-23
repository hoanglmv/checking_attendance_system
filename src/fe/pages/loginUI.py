import requests
from PyQt6 import QtCore, QtGui, QtWidgets
import re
from PyQt6.QtCore import QSettings, pyqtSignal, QObject
from PyQt6.QtGui import QCursor
from pages.informationUI import Ui_informationUI

class Ui_loginUI(QObject):  # Kế thừa từ QObject
    login_success = pyqtSignal()

    def __init__(self):
        super().__init__()  # Gọi hàm khởi tạo của QObject

    def setupUi(self, loginUI):
        loginUI.setObjectName("loginUI")
        loginUI.resize(750, 574)
        loginUI.setStyleSheet("background-color: #131A2D;")

        self.centralwidget = QtWidgets.QWidget(parent=loginUI)
        self.mainLayout = QtWidgets.QVBoxLayout(self.centralwidget)

        self.mainLayout.addStretch()  # Spacer trên

        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setFixedSize(500, 350)
        self.groupBox_2.setStyleSheet("background-color: #517078; border-radius: 10px;")
        self.innerLayout = QtWidgets.QVBoxLayout(self.groupBox_2)

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
        self.innerLayout.addWidget(self.login_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.actionLayout = QtWidgets.QHBoxLayout()
        
        self.register_button = QtWidgets.QPushButton("Đăng ký", self.groupBox_2)
        self.register_button.setStyleSheet(self.get_action_button_style())
        self.register_button.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.innerLayout.addLayout(self.actionLayout)

        self.forgot_button = QtWidgets.QPushButton("Quên mật khẩu", self.groupBox_2)
        self.forgot_button.setStyleSheet(self.get_action_button_style())
        self.forgot_button.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

        self.actionLayout.addWidget(self.register_button)
        self.actionLayout.addWidget(self.forgot_button)
        self.innerLayout.addLayout(self.actionLayout)

        self.mainLayout.addWidget(self.groupBox_2, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.mainLayout.addStretch()  # Spacer dưới

        loginUI.setLayout(self.mainLayout)

        self.error_label = QtWidgets.QLabel("", self.groupBox_2)
        self.error_label.setStyleSheet("color: red; font-size: 12pt;")
        self.error_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.innerLayout.addWidget(self.error_label)

        self.login_button.clicked.connect(self.validate_login_form)

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
            }
            QPushButton:hover {
                background-color: #31445B;
                border: 2px solid #FFD700;
            }
        """

    def get_action_button_style(self):
        return """
            QPushButton {
                color: #FFD700;
                font-size: 10pt;
                background: transparent;
                border: none;
            }
            QPushButton:hover {
                text-decoration: underline;
                color: #FFA500;
            }
        """

    def validate_login_form(self):
        email = self.inputs["email"].text().strip()
        password = self.inputs["password"].text().strip()

        if not email or not password:
            self.show_error("Cần phải điền đầy đủ thông tin!")
            return

        if not self.validate_email(email):
            self.show_error("Email không hợp lệ!")
            return

        self.error_label.setText("")  # Xóa thông báo lỗi nếu có
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
        login_data = {
            "email": email,
            "password": password,
        }

        try:
            response = requests.post(api_url, json=login_data)
            response.raise_for_status()  # Kiểm tra lỗi HTTP
            data = response.json()

            if "access_token" in data:
                settings = QSettings("MyApp", "LoginApp")
                access_token = data["access_token"]
                settings.setValue("access_token", access_token)
                print(f"Access Token saved: {access_token}")
                self.login_success.emit()
                self.clear_inputs()
            else:
                error_message = data.get("detail", "Đăng nhập thất bại! Kiểm tra lại thông tin.")
                print(f"Lỗi đăng nhập: {error_message}")
                self.show_error(error_message)

        except requests.RequestException as e:
            if hasattr(e, 'response') and e.response is not None:
                error_message = e.response.json().get("detail", f"Không thể kết nối đến máy chủ: {str(e)}")
                print(f"Lỗi kết nối đến API /auth/login: {error_message}")
                self.show_error(error_message)
            else:
                print("Không thể kết nối đến máy chủ! Kiểm tra xem backend có đang chạy không.")
                self.show_error("Không thể kết nối đến máy chủ! Kiểm tra xem backend có đang chạy không.")
        except Exception as e:
            print(f"Lỗi không xác định trong process_login: {str(e)}")
            self.show_error(f"Lỗi không xác định: {str(e)}")

    def clear_inputs(self):
        """Xóa nội dung các ô nhập liệu và thông báo lỗi"""
        print("Xóa nội dung các ô nhập liệu")
        for field in self.inputs:
            self.inputs[field].clear()  # Xóa nội dung ô nhập liệu
        self.error_label.setText("")  # Xóa thông báo lỗi
        print("Đã xóa các ô nhập liệu")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    loginUI = QtWidgets.QWidget()
    ui = Ui_loginUI()
    ui.setupUi(loginUI)
    loginUI.show()
    sys.exit(app.exec())