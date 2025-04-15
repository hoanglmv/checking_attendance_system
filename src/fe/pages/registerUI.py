import re
import sys
import requests
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import QObject

# Đường dẫn background GIF
BACKGROUND_GIF_PATH = r"D:\vhproj\checking_attendance_system\src\fe\Image_and_icon\CSS-Particles.gif"

from pages.OTPPopup import OTPPopUp

class Ui_registerUI(QObject):  # Kế thừa từ QObject
    def __init__(self):
        super().__init__()  # Gọi hàm khởi tạo của QObject

    def setupUi(self, registerUI):
        registerUI.setObjectName("registerUI")
        registerUI.resize(750, 950)
        # Thiết lập background mặc định (đã có màu), sau đó ta sẽ chồng background động lên
        registerUI.setStyleSheet("background-color: #131A2D;")
        
        # Thêm QLabel làm background với QMovie
        self.bg_label = QtWidgets.QLabel(registerUI)
        self.movie = QtGui.QMovie(BACKGROUND_GIF_PATH)
        self.bg_label.setMovie(self.movie)
        self.movie.start()
        self.bg_label.setScaledContents(True)
        self.bg_label.setGeometry(registerUI.rect())
        self.bg_label.lower()  # Đưa background về dưới cùng
        
        # Cài đặt eventFilter để cập nhật kích thước background khi cửa sổ thay đổi
        registerUI.installEventFilter(self)
        
        self.centralwidget = QtWidgets.QWidget(parent=registerUI)
        self.mainLayout = QtWidgets.QVBoxLayout(self.centralwidget)

        # Spacer để căn giữa theo chiều dọc
        self.mainLayout.addStretch()

        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setFixedSize(500, 580)
        self.groupBox_2.setStyleSheet("background-color: #517078; border-radius: 10px;")

        self.outerLayout = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.outerLayout.addStretch()

        self.centerWidget = QtWidgets.QWidget()
        self.centerWidget.setFixedSize(400, 580)
        self.innerLayout = QtWidgets.QVBoxLayout(self.centerWidget)
        self.outerLayout.addWidget(self.centerWidget)
        self.outerLayout.addStretch()

        # Tiêu đề đăng ký
        self.label = QtWidgets.QLabel("Đăng ký", self.groupBox_2)
        self.label.setStyleSheet("color: white; font: bold 20pt 'Times New Roman';")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.innerLayout.addWidget(self.label)

        # Các trường nhập liệu
        fields = ["full_name", "email", "phone", "position", "department", "password"]
        placeholders = ["Họ và tên", "Email", "Số điện thoại", "Vị trí", "Phòng ban", "Mật khẩu"]
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

        # Nút đăng ký
        self.register_button = QtWidgets.QPushButton("Đăng ký", self.groupBox_2)
        self.register_button.setFixedSize(250, 40)
        self.register_button.setStyleSheet(self.get_button_style())
        self.register_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.register_button.clicked.connect(self.validate_register_form)
        self.innerLayout.addWidget(self.register_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        # Label + nút đăng nhập
        self.loginLayout = QtWidgets.QHBoxLayout()
        self.login_label = QtWidgets.QLabel("Bạn đã có tài khoản?", self.groupBox_2)
        self.login_label.setStyleSheet("color: white; font-size: 11pt;")

        self.login_button = QtWidgets.QPushButton("Đăng nhập ngay", self.groupBox_2)
        self.login_button.setStyleSheet(self.get_login_button_style())
        self.login_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.login_button.clicked.connect(self.open_login)

        self.loginLayout.addWidget(self.login_label, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.loginLayout.addWidget(self.login_button, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        self.innerLayout.addLayout(self.loginLayout)

        self.mainLayout.addWidget(self.groupBox_2, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        # Spacer để căn giữa theo chiều dọc
        self.mainLayout.addStretch()

        registerUI.setLayout(self.mainLayout)

        # Thêm QLabel hiển thị thông báo lỗi
        self.error_label = QtWidgets.QLabel("", self.groupBox_2)
        self.error_label.setStyleSheet("color: red; font-size: 12pt;")
        self.error_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.innerLayout.addWidget(self.error_label)

    def eventFilter(self, obj, event):
        # Cập nhật lại kích thước của background khi cửa sổ thay đổi
        if event.type() == QtCore.QEvent.Type.Resize:
            obj_rect = obj.rect()
            self.bg_label.setGeometry(obj_rect)
        return super().eventFilter(obj, event)

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
                border: 2px solid #9FEF00;
            }
        """

    def get_login_button_style(self):
        return """
            QPushButton {
                color: #9FEF00;
                font-size: 10pt;
                background: transparent;
                border: none;
            }
            QPushButton:hover {
                text-decoration: underline;
                color: #9FEF00;
            }
        """

    def get_main_window(self):
        widget = self.centralwidget
        while widget.parent():
            widget = widget.parent()
        return widget

    def open_login(self):
        main_window = self.get_main_window()
        main_window.stacked_widget.setCurrentWidget(main_window.loginUI)

    def validate_email(self, email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email)

    def validate_register_form(self):
        for field_name, field in self.inputs.items():
            if not field.text().strip():
                self.error_label.setText("Cần phải điền đầy đủ thông tin!")
                return

        # Kiểm tra email hợp lệ
        email = self.inputs["email"].text().strip()
        if not self.validate_email(email):
            self.error_label.setText("Email không hợp lệ! Vui lòng nhập đúng định dạng.")
            return

        # Xóa thông báo lỗi nếu hợp lệ
        self.error_label.setText("")
        self.process_registration()

    def process_registration(self):
        url = "http://127.0.0.1:8000/auth/register"
        data = {
            "full_name": self.inputs["full_name"].text().strip(),
            "email": self.inputs["email"].text().strip(),
            "phone": self.inputs["phone"].text().strip(),
            "position": self.inputs["position"].text().strip(),
            "department": self.inputs["department"].text().strip(),
            "password": self.inputs["password"].text().strip(),
        }

        try:
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()  # Kiểm tra lỗi HTTP
            if response.status_code == 200:
                QtWidgets.QMessageBox.information(None, "Thành công", "Đăng ký thành công! Vui lòng kiểm tra email để xác thực.")
                email = data["email"]
                otp_dialog = OTPPopUp(email)
                if otp_dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                    QtWidgets.QMessageBox.information(None, "Thành công", "Xác minh thành công! Bạn có thể đăng nhập ngay.")
                    self.open_login()
                else:
                    QtWidgets.QMessageBox.warning(None, "Thất bại", "Xác minh OTP không thành công. Vui lòng thử lại.")
            else:
                error_message = response.json().get('detail', 'Đăng ký thất bại! Vui lòng thử lại.')
                QtWidgets.QMessageBox.warning(None, "Lỗi", f"Lỗi: {error_message}")
        except requests.exceptions.RequestException as e:
            if hasattr(e, 'response') and e.response is not None:
                error_message = e.response.json().get("detail", f"Không thể kết nối đến server: {str(e)}")
                QtWidgets.QMessageBox.critical(None, "Lỗi", error_message)
            else:
                QtWidgets.QMessageBox.critical(None, "Lỗi kết nối", "Không thể kết nối đến server. Vui lòng kiểm tra kết nối mạng!")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    registerUI = QtWidgets.QWidget()
    ui = Ui_registerUI()
    ui.setupUi(registerUI)
    registerUI.show()
    sys.exit(app.exec())
