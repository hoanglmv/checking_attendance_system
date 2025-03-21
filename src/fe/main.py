import sys
from PyQt6 import QtWidgets
from pages.registerUI import Ui_registerUI
from pages.loginUI import Ui_loginUI
from pages.informationUI import Ui_informationUI
from pages.OTPPopup import OTPPopUp
from PyQt6.QtCore import QSettings

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Checking Attendance System")
        self.setGeometry(100, 100, 800, 600)

        self.stacked_widget = QtWidgets.QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        # Tạo UI đăng nhập
        self.loginUI = QtWidgets.QMainWindow()
        self.ui_loginUI = Ui_loginUI()
        self.ui_loginUI.setupUi(self.loginUI)
        self.stacked_widget.addWidget(self.loginUI)

        # Tạo UI đăng ký
        self.registerUI = QtWidgets.QMainWindow()
        self.ui_registerUI = Ui_registerUI()
        self.ui_registerUI.setupUi(self.registerUI)
        self.stacked_widget.addWidget(self.registerUI)

        # Tạo UI thông tin (informationUI)
        self.informationUI = QtWidgets.QMainWindow()
        self.ui_informationUI = Ui_informationUI()
        self.ui_informationUI.setupUi(self.informationUI)
        self.stacked_widget.addWidget(self.informationUI)

        # Kiểm tra nút trước khi kết nối
        if hasattr(self.ui_loginUI, "register_button"):
            self.ui_loginUI.register_button.clicked.connect(self.go_to_registerUI)
        else:
            print("[LỖI] Không tìm thấy nút 'register_button' trong loginUI!")

        if hasattr(self.ui_registerUI, "login_button"):
            self.ui_registerUI.login_button.clicked.connect(self.go_to_loginUI)
        else:
            print("[LỖI] Không tìm thấy nút 'login_button' trong registerUI!")

        # Xóa access_token khi khởi động (tùy chọn)
        # settings = QSettings("MyApp", "LoginApp")
        # settings.remove("access_token")

        # Mặc định hiển thị Login UI
        self.stacked_widget.setCurrentWidget(self.loginUI)

        # Thêm biến giữ reference của OTPPopUp
        self.otp_popup = None

    def go_to_loginUI(self):
        self.stacked_widget.setCurrentWidget(self.loginUI)

    def go_to_registerUI(self):
        self.stacked_widget.setCurrentWidget(self.registerUI)

    def open_otp_popup(self, email):
        """Mở cửa sổ nhập OTP"""
        self.otp_popup = OTPPopUp(email)
        self.otp_popup.exec()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())