import requests
from PyQt6 import QtCore, QtGui, QtWidgets
import re
from PyQt6.QtCore import QSettings
from pages.informationUI import Ui_informationUI

class Ui_loginUI(object):
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
        self.login_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.innerLayout.addWidget(self.login_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.actionLayout = QtWidgets.QHBoxLayout()
        
        self.register_button = QtWidgets.QPushButton("Đăng ký", self.groupBox_2)
        self.register_button.setStyleSheet(self.get_action_button_style())
        self.register_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.register_button.clicked.connect(self.open_register)

        self.forgot_button = QtWidgets.QPushButton("Quên mật khẩu", self.groupBox_2)
        self.forgot_button.setStyleSheet(self.get_action_button_style())
        self.forgot_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

        self.actionLayout.addWidget(self.register_button)
        self.actionLayout.addWidget(self.forgot_button)
        self.innerLayout.addLayout(self.actionLayout)

        self.mainLayout.addWidget(self.groupBox_2, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.mainLayout.addStretch()  # Spacer dưới

        loginUI.setCentralWidget(self.centralwidget)

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

    def get_main_window(self):
        widget = self.centralwidget
        while widget.parent():
            widget = widget.parent()
        return widget
    
    def open_register(self):
        main_window = self.get_main_window()
        main_window.stacked_widget.setCurrentWidget(main_window.registerUI)

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
        api_url = "http://127.0.0.1:8000/auth/login"
        login_data = {
            "email": email,
            "password": password,
        }

        try:
            response = requests.post(api_url, json=login_data)
            data = response.json()

            if response.status_code == 200 and "access_token" in data:
                self.show_success("Đăng nhập thành công!")

                settings = QSettings("MyApp", "LoginApp")
                settings.setValue("access_token", data["access_token"])

                print("Access Token saved!")
                
                # Chuyển sang informationUI và tải dữ liệu nhân viên
                main_window = self.get_main_window()
                if not hasattr(main_window, 'informationUI'):
                    main_window.informationUI = QtWidgets.QMainWindow()
                    main_window.ui_informationUI = Ui_informationUI()
                    main_window.ui_informationUI.setupUi(main_window.informationUI)
                    main_window.stacked_widget.addWidget(main_window.informationUI)
                main_window.stacked_widget.setCurrentWidget(main_window.informationUI)
                main_window.ui_informationUI.load_employees_from_api()  # Tải dữ liệu sau khi đăng nhập
            else:
                error_message = data.get("detail", "Đăng nhập thất bại! Kiểm tra lại thông tin.")
                self.show_error(error_message)

        except requests.RequestException:
            self.show_error("Không thể kết nối đến máy chủ!")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    loginUI = QtWidgets.QMainWindow()
    ui = Ui_loginUI()
    ui.setupUi(loginUI)
    loginUI.show()
    sys.exit(app.exec())