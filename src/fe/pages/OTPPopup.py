import sys
import requests
from PyQt6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit,
    QPushButton, QMessageBox
)
from PyQt6.QtGui import QIntValidator, QFont
from PyQt6.QtCore import Qt, pyqtSignal

# API endpoint xác minh OTP
API_URL = "http://127.0.0.1:8000/auth/verify-otp"

class OTPPopUp(QDialog):

    otp_verified = pyqtSignal()
    def __init__(self, email):
        super().__init__()
        self.email = email
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
        layout.addWidget(self.resend_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def focus_next(self, index, text):
        """ Tự động chuyển sang ô tiếp theo khi nhập """
        if text and index < 5:
            self.otp_inputs[index + 1].setFocus()

    def get_otp_code(self):
        """ Lấy mã OTP từ các ô nhập """
        return "".join([box.text() for box in self.otp_inputs])

    def verify_otp(self):
        otp_code = self.get_otp_code()

        if len(otp_code) != 6:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ 6 chữ số OTP!")
            return # Không tiếp tục xử lý nếu OTP chưa đủ 6 số

        try:
            email_cleaned = self.email.strip()  # Loại bỏ khoảng trắng/thừa ký tự
            otp_code = self.get_otp_code().strip()
            # Gửi yêu cầu xác minh OTP đến API
            response = requests.post(API_URL, params={"email": email_cleaned, "otp": otp_code})

            if response.status_code == 200:
                QMessageBox.information(self, "Thành công", "Xác minh thành công!")
                self.otp_verified.emit()  # Phát tín hiệu thành công
                self.accept()  # Đóng cửa sổ OTP
                
            else:
                # Lấy thông báo lỗi từ API hoặc hiển thị lỗi mặc định
                error_msg = response.json().get("detail", "OTP không đúng, vui lòng nhập lại.")
                QMessageBox.warning(self, "Lỗi", error_msg)  # Dùng warning thay vì critical

                # Xóa dữ liệu trong các ô nhập OTP để người dùng nhập lại
                for box in self.otp_inputs:
                    box.clear()

                # Đưa con trỏ về ô nhập đầu tiên
                self.otp_inputs[0].setFocus()

                # Không gọi `reject()` hoặc `accept()` để tránh đóng cửa sổ

        except requests.RequestException:
            QMessageBox.warning(self, "Lỗi", "Không thể kết nối đến máy chủ, vui lòng thử lại!")

            # Không cho phép đóng cửa sổ khi gặp lỗi mạng
            return
        
    def main_style(self):
        """ Định dạng giao diện tổng thể """
        return """
            QDialog {
                background-color: #1B263B;
                border-radius: 10px;
            }
        """

    def input_style(self):
        """ Định dạng ô nhập OTP """
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
        """ Định dạng nút xác minh """
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
        """ Định dạng nút gửi lại OTP """
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

# Chạy thử pop-up
if __name__ == "__main__":
    app = QApplication(sys.argv)
    email = "user@example.com"
    otp_dialog = OTPPopUp(email)

    if otp_dialog.exec() == QDialog.DialogCode.Accepted:
        print("✅ Xác minh thành công!")
    else:
        print("❌ Xác minh thất bại hoặc bị hủy.")

    # ❌ KHÔNG dùng sys.exit() ở đây nếu bạn không muốn đóng toàn bộ ứng dụng
    app.exec()