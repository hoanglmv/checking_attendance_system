import sys
import requests
import re
from PyQt6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit,
    QPushButton, QMessageBox, QWidget, QGroupBox
)
from PyQt6.QtGui import QIntValidator, QFont, QCursor, QMovie
from PyQt6.QtCore import Qt, pyqtSignal, QObject

# API endpoints
FORGOT_PASSWORD_URL = "http://127.0.0.1:8000/auth/forgot-password"
VERIFY_OTP_URL = "http://127.0.0.1:8000/auth/verify-otp"
VERIFY_OTP_FORGOT_PASSWORD_URL = "http://127.0.0.1:8000/auth/verify-otp-forgot-password"
RESET_PASSWORD_URL = "http://127.0.0.1:8000/auth/reset-password"

BACKGROUND_GIF_PATH = r"D:\vhproj\checking_attendance_system\src\fe\Image_and_icon\CSS-Particles.gif"

class EnterEmailUI(QWidget):
    email_submitted = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.set_background()   # Thiết lập background cho widget
        self.initUI()

    def set_background(self):
        # Tạo QLabel để hiển thị background động
        self.bg_label = QLabel(self)
        self.movie = QMovie(BACKGROUND_GIF_PATH)
        self.bg_label.setMovie(self.movie)
        self.movie.start()
        self.bg_label.setScaledContents(True)
        self.bg_label.setGeometry(self.rect())
        self.bg_label.lower()  # Đưa background xuống dưới các widget khác

    def resizeEvent(self, event):
        self.bg_label.setGeometry(self.rect())
        return super().resizeEvent(event)

    def initUI(self):
        # Layout chính của widget, các widget con sẽ được đặt phía trên background
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.addStretch()

        # Tạo QGroupBox như giao diện đăng nhập
        self.groupBox_2 = QGroupBox(self)
        self.groupBox_2.setFixedSize(500, 350)
        self.groupBox_2.setStyleSheet("background-color: #517078; border-radius: 10px;")
        self.innerLayout = QVBoxLayout(self.groupBox_2)

        # Tiêu đề
        self.label = QLabel("Nhập email", self.groupBox_2)
        self.label.setStyleSheet("color: white; font: bold 20pt 'Times New Roman';")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.innerLayout.addWidget(self.label)

        # Ô nhập email
        self.email_input = QLineEdit(self.groupBox_2)
        self.email_input.setPlaceholderText("Email")
        self.email_input.setFixedHeight(45)
        self.email_input.setStyleSheet(self.input_style())
        self.innerLayout.addWidget(self.email_input)

        # Nút gửi mã OTP
        self.submit_button = QPushButton("Gửi mã OTP", self.groupBox_2)
        self.submit_button.setFixedSize(250, 40)
        self.submit_button.setStyleSheet(self.get_button_style())
        self.submit_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.submit_button.clicked.connect(self.submit_email)
        self.innerLayout.addWidget(self.submit_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Nút quay lại đăng nhập
        self.actionLayout = QHBoxLayout()
        self.back_to_login = QPushButton("Quay lại đăng nhập", self.groupBox_2)
        self.back_to_login.setStyleSheet(self.get_action_button_style())
        self.back_to_login.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.back_to_login.clicked.connect(self.open_login)
        self.actionLayout.addStretch()
        self.actionLayout.addWidget(self.back_to_login)
        self.actionLayout.addStretch()
        self.innerLayout.addLayout(self.actionLayout)

        self.mainLayout.addWidget(self.groupBox_2, alignment=Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addStretch()

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

    def validate_email(self, email):
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(email_regex, email) is not None

    def submit_email(self):
        email = self.email_input.text().strip()
        if not email:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập email!")
            return
        if not self.validate_email(email):
            QMessageBox.warning(self, "Lỗi", "Email không hợp lệ!")
            return
        try:
            response = requests.post(FORGOT_PASSWORD_URL, json={"email": email})
            response.raise_for_status()
            QMessageBox.information(self, "Thành Công", "Mã OTP đã được gửi đến email của bạn! Vui lòng kiểm tra email và nhập mã OTP.")
            self.email_submitted.emit(email)
        except requests.RequestException as e:
            error_message = e.response.json().get("detail", "Không thể gửi mã OTP. Vui lòng kiểm tra email và thử lại.") if e.response else str(e)
            QMessageBox.warning(self, "Lỗi", error_message)

    def get_main_window(self):
        widget = self
        while widget.parent():
            widget = widget.parent()
        return widget

    def open_login(self):
        main_window = self.get_main_window()
        main_window.stacked_widget.setCurrentWidget(main_window.loginUI)

class OTPPopUp(QDialog):
    otp_verified = pyqtSignal(str)

    def __init__(self, email, is_for_registration=False):
        super().__init__()
        self.email = email
        self.is_for_registration = is_for_registration
        self.setWindowTitle("Nhập mã OTP")
        self.setFixedSize(400, 250)
        self.set_background()   # Thiết lập background cho dialog
        self.initUI()

    def set_background(self):
        self.bg_label = QLabel(self)
        self.movie = QMovie(BACKGROUND_GIF_PATH)
        self.bg_label.setMovie(self.movie)
        self.movie.start()
        self.bg_label.setScaledContents(True)
        self.bg_label.setGeometry(self.rect())
        self.bg_label.lower()

    def resizeEvent(self, event):
        self.bg_label.setGeometry(self.rect())
        return super().resizeEvent(event)

    def initUI(self):
        layout = QVBoxLayout()
        self.label = QLabel("Nhập mã OTP (6 số) được gửi qua email:")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(QFont("Times New Roman", 12))
        self.label.setStyleSheet("color: white;")
        layout.addWidget(self.label)

        self.otp_inputs = []
        otp_layout = QHBoxLayout()
        for i in range(6):
            otp_input = QLineEdit()
            otp_input.setFixedSize(50, 50)
            otp_input.setMaxLength(1)
            otp_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
            otp_input.setValidator(QIntValidator(0, 9))
            otp_input.setStyleSheet(self.input_style())
            otp_input.textChanged.connect(lambda text, idx=i: self.focus_next(idx, text))
            self.otp_inputs.append(otp_input)
            otp_layout.addWidget(otp_input)
        layout.addLayout(otp_layout)

        self.verify_btn = QPushButton("Xác minh")
        self.verify_btn.setStyleSheet(self.get_button_style())
        self.verify_btn.clicked.connect(self.verify_otp)
        layout.addWidget(self.verify_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.resend_btn = QPushButton("Gửi lại OTP")
        self.resend_btn.setStyleSheet(self.get_login_button_style())
        self.resend_btn.clicked.connect(self.resend_otp)
        layout.addWidget(self.resend_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def focus_next(self, index, text):
        if text and index < 5:
            self.otp_inputs[index + 1].setFocus()

    def get_otp_code(self):
        return "".join([box.text() for box in self.otp_inputs])

    def verify_otp(self):
        otp_code = self.get_otp_code()
        if len(otp_code) != 6:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ 6 chữ số OTP!")
            return
        try:
            email_cleaned = self.email.strip()
            otp_code = self.get_otp_code().strip()
            url = VERIFY_OTP_URL if self.is_for_registration else VERIFY_OTP_FORGOT_PASSWORD_URL
            response = requests.post(url, params={"email": email_cleaned, "otp": otp_code})
            response.raise_for_status()
            QMessageBox.information(self, "Thành Công", "Xác minh thành công!")
            self.otp_verified.emit(self.email)
            self.accept()
        except requests.RequestException as e:
            error_message = e.response.json() if e.response else str(e)
            QMessageBox.warning(self, "Lỗi", str(error_message))
            for box in self.otp_inputs:
                box.clear()
            self.otp_inputs[0].setFocus()

    def resend_otp(self):
        try:
            response = requests.post(FORGOT_PASSWORD_URL, json={"email": self.email})
            response.raise_for_status()
            QMessageBox.information(self, "Thành Công", "Mã OTP mới đã được gửi đến email của bạn!")
        except requests.RequestException as e:
            error_message = e.response.json().get("detail", "Không thể gửi mã OTP. Vui lòng thử lại.") if e.response else str(e)
            QMessageBox.warning(self, "Lỗi", error_message)

    def input_style(self):
        return """
            QLineEdit {
                border: 2px solid white;
                border-radius: 10px;
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 5px;
                background-color: transparent;
                text-align: center;
            }
            QLineEdit:focus {
                border: 2px solid #FFD700;
            }
        """

    def get_button_style(self):
        return """
            QPushButton {
                border: 2px solid white;
                color: white;
                font: bold 12pt 'Times New Roman';
                border-radius: 10px;
                background-color: #415A77;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #31445B;
                border: 2px solid #FFD700;
            }
        """

    def get_login_button_style(self):
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

class ResetPasswordUI(QWidget):
    password_reset_success = pyqtSignal()

    def __init__(self, email, otp):
        super().__init__()
        self.email = email
        self.otp = otp
        self.set_background()   # Thiết lập background cho widget
        self.initUI()

    def set_background(self):
        self.bg_label = QLabel(self)
        self.movie = QMovie(BACKGROUND_GIF_PATH)
        self.bg_label.setMovie(self.movie)
        self.movie.start()
        self.bg_label.setScaledContents(True)
        self.bg_label.setGeometry(self.rect())
        self.bg_label.lower()

    def resizeEvent(self, event):
        self.bg_label.setGeometry(self.rect())
        return super().resizeEvent(event)

    def initUI(self):
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.addStretch()

        # Tạo QGroupBox như giao diện đăng nhập
        self.groupBox_2 = QGroupBox(self)
        self.groupBox_2.setFixedSize(500, 350)
        self.groupBox_2.setStyleSheet("background-color: #517078; border-radius: 10px;")
        self.innerLayout = QVBoxLayout(self.groupBox_2)

        # Tiêu đề
        self.label = QLabel("Đặt lại mật khẩu", self.groupBox_2)
        self.label.setStyleSheet("color: white; font: bold 20pt 'Times New Roman';")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.innerLayout.addWidget(self.label)

        # Ô nhập mật khẩu mới
        self.new_password = QLineEdit(self.groupBox_2)
        self.new_password.setPlaceholderText("Mật khẩu mới")
        self.new_password.setFixedHeight(45)
        self.new_password.setStyleSheet(self.input_style())
        self.new_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.innerLayout.addWidget(self.new_password)

        # Ô xác nhận mật khẩu
        self.confirm_password = QLineEdit(self.groupBox_2)
        self.confirm_password.setPlaceholderText("Xác nhận mật khẩu")
        self.confirm_password.setFixedHeight(45)
        self.confirm_password.setStyleSheet(self.input_style())
        self.confirm_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.innerLayout.addWidget(self.confirm_password)

        # Nút đặt lại mật khẩu
        self.reset_button = QPushButton("Đặt lại mật khẩu", self.groupBox_2)
        self.reset_button.setFixedSize(250, 40)
        self.reset_button.setStyleSheet(self.get_button_style())
        self.reset_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.reset_button.clicked.connect(self.reset_password)
        self.innerLayout.addWidget(self.reset_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.mainLayout.addWidget(self.groupBox_2, alignment=Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addStretch()

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

    def reset_password(self):
        new_password = self.new_password.text().strip()
        confirm_password = self.confirm_password.text().strip()
        if not new_password or not confirm_password:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return
        if new_password != confirm_password:
            QMessageBox.warning(self, "Lỗi", "Mật khẩu mới và mật khẩu xác nhận không khớp!")
            return
        if len(new_password) < 8:
            QMessageBox.warning(self, "Lỗi", "Mật khẩu mới phải có ít nhất 8 ký tự!")
            return
        try:
            response = requests.post(RESET_PASSWORD_URL, json={
                "email": self.email,
                "otp": self.otp,
                "new_password": new_password,
                "confirm_password": confirm_password
            })
            response.raise_for_status()
            QMessageBox.information(self, "Thành Công", "Mật khẩu đã được đặt lại thành công! Vui lòng đăng nhập lại.")
            self.password_reset_success.emit()
        except requests.RequestException as e:
            error_message = e.response.json().get("detail", "Không thể đặt lại mật khẩu. Vui lòng thử lại.") if e.response else str(e)
            QMessageBox.warning(self, "Lỗi", error_message)

class ForgotPasswordUI(QObject):
    def __init__(self):
        super().__init__()
        self.enter_email_ui = None
        self.otp_popup = None
        self.reset_password_ui = None
        self.setupUi()

    def setupUi(self):
        self.enter_email_ui = EnterEmailUI()

    def get_main_window(self):
        widget = self.enter_email_ui
        while widget.parent():
            widget = widget.parent()
        return widget

    def open_login(self):
        main_window = self.get_main_window()
        main_window.stacked_widget.setCurrentWidget(main_window.loginUI)

    def show_otp_popup(self, email):
        self.otp_popup = OTPPopUp(email, is_for_registration=False)
        self.otp_popup.otp_verified.connect(lambda verified_email: self.show_reset_password(verified_email, self.otp_popup.get_otp_code()))
        if self.otp_popup.exec() == QDialog.DialogCode.Accepted:
            self.get_main_window().stacked_widget.setCurrentWidget(self.reset_password_ui)
        else:
            self.get_main_window().stacked_widget.setCurrentWidget(self.enter_email_ui)

    def show_reset_password(self, email, otp):
        self.reset_password_ui = ResetPasswordUI(email, otp)
        self.get_main_window().stacked_widget.setCurrentWidget(self.reset_password_ui)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Ví dụ khởi chạy giao diện nhập email cho chức năng quên mật khẩu
    forgot_password_ui = EnterEmailUI()
    forgot_password_ui.show()
    app.exec()
