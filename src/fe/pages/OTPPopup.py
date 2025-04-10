import sys
import requests
from PyQt6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit,
    QPushButton, QMessageBox
)
from PyQt6.QtGui import QIntValidator, QFont
from PyQt6.QtCore import Qt, pyqtSignal

# API endpoints
VERIFY_OTP_URL = "http://127.0.0.1:8000/auth/verify-otp"
VERIFY_OTP_FORGOT_PASSWORD_URL = "http://127.0.0.1:8000/auth/verify-otp-forgot-password"
FORGOT_PASSWORD_URL = "http://127.0.0.1:8000/auth/forgot-password"

class OTPPopUp(QDialog):
    # Định nghĩa tín hiệu với một tham số str (email)
    otp_verified = pyqtSignal(str)  

    def __init__(self, email, is_for_registration=True):
        super().__init__()
        self.email = email
        self.is_for_registration = is_for_registration
        self.setWindowTitle("Nhập mã OTP")
        self.setFixedSize(400, 250)
        self.initUI()
        self.setStyleSheet(self.main_style())

    def initUI(self):
        layout = QVBoxLayout()

        # Tiêu đề
        self.label = QLabel("Nhập mã OTP (6 số) được gửi qua email:")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(QFont("Times New Roman", 12))
        self.label.setStyleSheet("color: white;")
        layout.addWidget(self.label)

        # Hàng chứa 6 ô nhập OTP
        self.otp_inputs = []
        otp_layout = QHBoxLayout()

        for i in range(6):
            otp_input = QLineEdit()
            otp_input.setFixedSize(50, 50)
            otp_input.setMaxLength(1)  # Giới hạn 1 ký tự
            otp_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
            otp_input.setValidator(QIntValidator(0, 9))  # Chỉ cho phép nhập số
            otp_input.setStyleSheet(self.input_style())
            otp_input.textChanged.connect(lambda text, idx=i: self.focus_next(idx, text))
            self.otp_inputs.append(otp_input)
            otp_layout.addWidget(otp_input)

        layout.addLayout(otp_layout)

        # Nút Xác minh OTP
        self.verify_btn = QPushButton("Xác minh")
        self.verify_btn.setStyleSheet(self.get_button_style())
        self.verify_btn.clicked.connect(self.verify_otp)
        layout.addWidget(self.verify_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        # Nút Gửi lại OTP
        self.resend_btn = QPushButton("Gửi lại OTP")
        self.resend_btn.setStyleSheet(self.get_login_button_style())
        self.resend_btn.clicked.connect(self.resend_otp)
        layout.addWidget(self.resend_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def focus_next(self, index, text):
        """Tự động chuyển sang ô tiếp theo khi nhập."""
        if text and index < 5:
            self.otp_inputs[index + 1].setFocus()

    def get_otp_code(self):
        """Lấy mã OTP từ các ô nhập."""
        return "".join([box.text() for box in self.otp_inputs])

    def verify_otp(self):
        otp_code = self.get_otp_code()

        if len(otp_code) != 6:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ 6 chữ số OTP!")
            return

        try:
            email_cleaned = self.email.strip()
            otp_code = self.get_otp_code().strip()
            # Chọn URL dựa trên luồng
            url = VERIFY_OTP_URL if self.is_for_registration else VERIFY_OTP_FORGOT_PASSWORD_URL
            print(f"is_for_registration: {self.is_for_registration}, Using URL: {url}")
            # Gửi yêu cầu xác minh OTP đến API qua query parameters
            response = requests.post(url, params={"email": email_cleaned, "otp": otp_code})
            
            response.raise_for_status()
            QMessageBox.information(self, "Thành Công", "Xác minh thành công!")
            # Luôn phát tín hiệu với email, bất kể là đăng ký hay quên mật khẩu
            self.otp_verified.emit(self.email)
            self.accept()  # Đóng dialog sau khi xác minh thành công
        except requests.RequestException as e:
            error_message = e.response.json() if e.response else str(e)
            print(f"Error response from server: {error_message}")
            QMessageBox.warning(self, "Lỗi", str(error_message))
            for box in self.otp_inputs:
                box.clear()
            self.otp_inputs[0].setFocus()
        except Exception as e:
            print(f"Lỗi không xác định trong verify_otp: {str(e)}")
            QMessageBox.critical(self, "Lỗi", f"Có lỗi xảy ra: {str(e)}. Vui lòng thử lại!")
            for box in self.otp_inputs:
                box.clear()
            self.otp_inputs[0].setFocus()

    def resend_otp(self):
        """Gửi lại mã OTP."""
        try:
            response = requests.post(FORGOT_PASSWORD_URL, json={"email": self.email})
            response.raise_for_status()
            QMessageBox.information(self, "Thành Công", "Mã OTP mới đã được gửi đến email của bạn!")
        except requests.RequestException as e:
            error_message = e.response.json().get("detail", "Không thể gửi mã OTP. Vui lòng thử lại.") if e.response else str(e)
            QMessageBox.warning(self, "Lỗi", error_message)
        except Exception as e:
            print(f"Lỗi không xác định trong resend_otp: {str(e)}")
            QMessageBox.critical(self, "Lỗi", f"Có lỗi xảy ra khi gửi lại OTP: {str(e)}. Vui lòng thử lại!")

    def main_style(self):
        """Định dạng giao diện tổng thể."""
        return """
            QDialog {
                background-color: #1B263B;
                border-radius: 10px;
            }
        """

    def input_style(self):
        """Định dạng ô nhập OTP."""
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
        """Định dạng nút xác minh."""
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
        """Định dạng nút gửi lại OTP."""
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    email = "user@example.com"
    # Thử cho đăng ký
    otp_dialog = OTPPopUp(email, is_for_registration=True)
    if otp_dialog.exec() == QDialog.DialogCode.Accepted:
        print("✅ Xác minh thành công (đăng ký)!")
    else:
        print("❌ Xác minh thất bại hoặc bị hủy (đăng ký).")
    
    # Thử cho quên mật khẩu
    otp_dialog = OTPPopUp(email, is_for_registration=False)
    if otp_dialog.exec() == QDialog.DialogCode.Accepted:
        print("✅ Xác minh thành công (quên mật khẩu)!")
    else:
        print("❌ Xác minh thất bại hoặc bị hủy (quên mật khẩu).")

    app.exec()