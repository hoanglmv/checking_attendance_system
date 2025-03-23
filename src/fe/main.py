import sys
from PyQt6 import QtWidgets
from pages.registerUI import Ui_registerUI
from pages.loginUI import Ui_loginUI
from pages.informationUI import Ui_informationUI
from pages.OTPPopup import OTPPopUp
from PyQt6.QtCore import QSettings
import requests

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Checking Attendance System")
        self.setGeometry(100, 100, 1280, 720)

        self.stacked_widget = QtWidgets.QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        # Tạo UI đăng nhập
        self.loginUI = QtWidgets.QWidget()
        self.ui_loginUI = Ui_loginUI()
        self.ui_loginUI.setupUi(self.loginUI)
        self.stacked_widget.addWidget(self.loginUI)

        # Tạo UI đăng ký
        self.registerUI = QtWidgets.QWidget()
        self.ui_registerUI = Ui_registerUI()
        self.ui_registerUI.setupUi(self.registerUI)
        self.stacked_widget.addWidget(self.registerUI)

        # Tạo UI thông tin (informationUI)
        self.informationUI = QtWidgets.QWidget()
        self.ui_informationUI = Ui_informationUI()
        self.ui_informationUI.setupUi(self.informationUI, self.stacked_widget)
        self.stacked_widget.addWidget(self.informationUI)

        # Kiểm tra và kết nối các nút
        if hasattr(self.ui_loginUI, "register_button"):
            self.ui_loginUI.register_button.clicked.connect(self.go_to_registerUI)
        else:
            QtWidgets.QMessageBox.critical(self, "Lỗi", "Không tìm thấy nút 'register_button' trong loginUI!")
            sys.exit(1)

        if hasattr(self.ui_registerUI, "login_button"):
            self.ui_registerUI.login_button.clicked.connect(self.go_to_loginUI)
        else:
            QtWidgets.QMessageBox.critical(self, "Lỗi", "Không tìm thấy nút 'login_button' trong registerUI!")
            sys.exit(1)

        # Kết nối tín hiệu từ loginUI để chuyển sang informationUI sau khi đăng nhập
        self.ui_loginUI.login_success.connect(self.on_login_success)

        # Kết nối tín hiệu đăng xuất từ Sidebar
        self.ui_informationUI.sidebar.logout_signal.connect(self.handle_logout)

        # Hiển thị giao diện đăng nhập khi khởi động
        self.check_login_status()

        # Thêm biến giữ reference của OTPPopUp
        self.otp_popup = None

    def check_login_status(self):
        """Hiển thị giao diện đăng nhập khi khởi động"""
        print("Hiển thị loginUI khi khởi động")
        self.stacked_widget.setCurrentWidget(self.loginUI)

    def go_to_loginUI(self):
        self.stacked_widget.setCurrentWidget(self.loginUI)

    def go_to_registerUI(self):
        self.stacked_widget.setCurrentWidget(self.registerUI)

    def on_login_success(self):
        """Chuyển sang informationUI sau khi đăng nhập thành công"""
        print("Đăng nhập thành công, chuyển sang informationUI")
        self.stacked_widget.setCurrentWidget(self.informationUI)
        self.ui_informationUI.load_employees_from_api()
        # Cập nhật thông tin admin sau khi đăng nhập
        self.ui_informationUI.header.refresh_admin_info()

    def handle_logout(self):
        """Xử lý đăng xuất: Chuyển về loginUI và xóa nội dung ô nhập liệu"""
        print("MainWindow nhận tín hiệu đăng xuất")
        self.stacked_widget.setCurrentWidget(self.loginUI)
        self.ui_loginUI.clear_inputs()
        print("Đã chuyển về loginUI và xóa nội dung ô nhập liệu")

    def open_otp_popup(self, email):
        """Mở cửa sổ nhập OTP"""
        if self.otp_popup is not None:
            self.otp_popup.close()
        self.otp_popup = OTPPopUp(email)
        self.otp_popup.exec()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())