from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QApplication
)
from PyQt6.QtGui import QIntValidator
from PyQt6.QtCore import Qt
import sys

class OtpPopup(QDialog):
    def __init__(self, email="example@gmail.com"):
        super().__init__()

        self.setWindowTitle("Nhập mã OTP")
        self.setFixedSize(350, 200)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)  
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_label = QLabel("Nhập mã OTP")
        title_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        email_label = QLabel(f"Mã OTP đã được gửi đến email:\n {email}")
        email_label.setStyleSheet("color: white; font-size: 14px;")
        email_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(email_label)

        otp_layout = QHBoxLayout()
        self.otp_fields = []

        for i in range(6):
            otp_input = QLineEdit(self)
            otp_input.setMaxLength(1)  
            otp_input.setValidator(QIntValidator(0, 9, self))  
            otp_input.setFixedSize(40, 40)
            otp_input.setAlignment(Qt.AlignmentFlag.AlignCenter)  
            otp_input.setStyleSheet(
                "font-size: 18px; color: white; background-color: #253B54; border: 2px solid #3A5A80; border-radius: 5px;"
            )

            otp_input.textChanged.connect(lambda _, idx=i: self.move_next(idx))  
            self.otp_fields.append(otp_input)
            otp_layout.addWidget(otp_input)

        layout.addLayout(otp_layout)

        self.submit_button = QPushButton("Xác nhận OTP")
        self.submit_button.setStyleSheet(
            "background-color: #28a745; color: white; font-size: 16px; padding: 8px; border-radius: 5px;"
        )
        self.submit_button.clicked.connect(self.get_otp)
        layout.addWidget(self.submit_button)

        resend_layout = QHBoxLayout()
        not_received_label = QLabel("Không nhận được mã?")
        not_received_label.setStyleSheet("color: white; font-size: 14px;")

        self.resend_button = QPushButton("Gửi lại OTP")
        self.resend_button.setStyleSheet(
            "background: none; color: #1E90FF; font-size: 14px; border: none; text-decoration: underline;"
        )
        self.resend_button.clicked.connect(self.resend_otp)

        resend_layout.addWidget(not_received_label)
        resend_layout.addWidget(self.resend_button)
        layout.addLayout(resend_layout)

        self.setLayout(layout)
        self.setStyleSheet("background-color: #192E44; border-radius: 10px;")

    def move_next(self, index):
        if index < 5 and self.otp_fields[index].text():
            self.otp_fields[index + 1].setFocus()

    def get_otp(self):
        otp_code = ''.join(field.text() for field in self.otp_fields)
        print("OTP Nhập:", otp_code)
        self.accept()  

    def resend_otp(self):
        print("Gửi lại OTP...")  

if __name__ == "__main__":
    app = QApplication(sys.argv)
    email = "kien45671duong@gmail.com"  
    dialog = OtpPopup(email)
    if dialog.exec():
        print("OTP đã nhập:", ''.join(field.text() for field in dialog.otp_fields))
    sys.exit(app.exec())
