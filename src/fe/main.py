import sys
from PyQt6 import QtWidgets
from PyQt6.QtCore import QSettings, QTimer
from pages.registerUI import Ui_registerUI
from pages.loginUI import Ui_loginUI
from pages.informationUI import Ui_informationUI
from pages.checkingUI import CheckingUI
from pages.checkingUI_2 import CheckingUI_2
from pages.OTPPopup import OTPPopUp
from pages.forgotPasswordUI import ForgotPasswordUI, EnterEmailUI, ResetPasswordUI
import requests
import traceback

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Checking Attendance System")
        self.setGeometry(100, 100, 1280, 720)

        # Đặt màu nền cho MainWindow
        self.setStyleSheet("background-color: #131A2D;")

        self.stacked_widget = QtWidgets.QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        # Khởi tạo loginUI
        print("Khởi tạo loginUI")
        self.loginUI = QtWidgets.QWidget()
        self.ui_loginUI = Ui_loginUI()
        self.ui_loginUI.setupUi(self.loginUI)
        self.stacked_widget.addWidget(self.loginUI)

        # Khởi tạo registerUI
        print("Khởi tạo registerUI")
        self.registerUI = QtWidgets.QWidget()
        self.ui_registerUI = Ui_registerUI()
        self.ui_registerUI.setupUi(self.registerUI)
        self.stacked_widget.addWidget(self.registerUI)

        # Khởi tạo informationUI
        print("Khởi tạo informationUI")
        self.informationUI = QtWidgets.QWidget()
        self.ui_informationUI = Ui_informationUI()
        self.ui_informationUI.setupUi(self.informationUI, self.stacked_widget)
        self.stacked_widget.addWidget(self.informationUI)

        # Khởi tạo checkingUI
        print("Khởi tạo checkingUI")
        self.checkingUI = CheckingUI()
        self.stacked_widget.addWidget(self.checkingUI)

        # Khởi tạo checkingUI_2
        print("Khởi tạo checkingUI_2")
        self.checkingUI_2 = CheckingUI_2(self.stacked_widget)
        self.stacked_widget.addWidget(self.checkingUI_2)

        # Khởi tạo forgotPasswordUI
        print("Khởi tạo forgotPasswordUI")
        self.forgotPasswordUI = ForgotPasswordUI()
        self.stacked_widget.addWidget(self.forgotPasswordUI.enter_email_ui)
        # Placeholder cho reset_password_ui, sẽ được cập nhật sau khi tạo
        self.reset_password_placeholder = QtWidgets.QWidget()
        self.stacked_widget.addWidget(self.reset_password_placeholder)

        # Kết nối các sự kiện từ loginUI và registerUI
        if hasattr(self.ui_loginUI, "register_button"):
            self.ui_loginUI.register_button.clicked.connect(self.go_to_registerUI)
        if hasattr(self.ui_registerUI, "login_button"):
            self.ui_registerUI.login_button.clicked.connect(self.goINSIDE_to_loginUI)
        self.ui_loginUI.login_success.connect(self.on_login_success)
        if hasattr(self.ui_loginUI, "forgot_button"):
            self.ui_loginUI.forgot_button.clicked.connect(self.go_to_forgot_passwordUI)

        # Kết nối tín hiệu từ các giao diện
        self.ui_informationUI.sidebar.logout_signal.connect(self.handle_logout)
        self.ui_informationUI.logout_signal.connect(self.handle_logout)
        self.ui_informationUI.sidebar.attendance_signal.connect(self.go_to_checkingUI)
        self.ui_informationUI.sidebar.manage_signal.connect(self.go_to_informationUI)
        self.checkingUI.ui.sidebar.logout_signal.connect(self.handle_logout)
        self.checkingUI.ui.sidebar.attendance_signal.connect(self.go_to_checkingUI)
        self.checkingUI.ui.sidebar.manage_signal.connect(self.go_to_informationUI)
        self.checkingUI_2.ui.sidebar.logout_signal.connect(self.handle_logout)
        self.checkingUI_2.ui.sidebar.attendance_signal.connect(self.go_to_checkingUI)
        self.checkingUI_2.ui.sidebar.manage_signal.connect(self.go_to_informationUI)

        self.checkingUI.switch_to_day_signal.connect(self.go_to_checkingUI)
        self.checkingUI.switch_to_month_signal.connect(self.go_to_checkingUI_2)
        self.checkingUI_2.switch_to_day_signal.connect(self.go_to_checkingUI)
        self.checkingUI_2.switch_to_month_signal.connect(self.go_to_checkingUI_2)

        # Kết nối sự kiện từ listChecking_2 đến attendance_calendar
        self.checkingUI_2.ui.employee_row.employeeList.itemClicked.connect(self.checkingUI_2.ui.content.on_employee_clicked)

        # Kết nối tín hiệu từ ForgotPasswordUI
        self.forgotPasswordUI.enter_email_ui.back_to_login.clicked.connect(self.goINSIDE_to_loginUI)
        self.forgotPasswordUI.enter_email_ui.email_submitted.connect(self.open_otp_popup_for_forgot_password)

        self.check_login_status()
        self.otp_popup = None

    def on_login_success(self):
        print("Đăng nhập thành công")
        settings = QSettings("MyApp", "LoginApp")
        token = settings.value("access_token", None)
        print(f"Token từ QSettings trong on_login_success: {token}")
        
        if token:
            try:
                print(f"Token đã sẵn sàng: {token}")
                self.stacked_widget.setCurrentWidget(self.informationUI)
                QTimer.singleShot(100, self.load_information_ui_data)
                QTimer.singleShot(100, self.checkingUI_2.on_login_success)
            except Exception as e:
                print(f"Lỗi khi chuyển giao diện hoặc tải dữ liệu: {str(e)}")
                traceback.print_exc()
                self.stacked_widget.setCurrentWidget(self.loginUI)
        else:
            print("Không có token trong QSettings sau đăng nhập!")
            self.stacked_widget.setCurrentWidget(self.loginUI)
        
        print("Đã xử lý đăng nhập thành công")

    def load_information_ui_data(self):
        settings = QSettings("MyApp", "LoginApp")
        token = settings.value("access_token", None)
        print(f"Token trước khi gọi load_employees_from_api trong load_information_ui_data: {token}")
        if token:
            try:
                self.ui_informationUI.load_employees_from_api()
                self.ui_informationUI.header.refresh_admin_info()
            except Exception as e:
                print(f"Lỗi trong load_information_ui_data: {str(e)}")
                traceback.print_exc()
        else:
            print("Không có token, chuyển về loginUI")
            self.handle_logout()

    def handle_logout(self):
        print("MainWindow nhận tín hiệu đăng xuất")
        settings = QSettings("MyApp", "LoginApp")
        settings.remove("access_token")
        settings.sync()
        print("Đã xóa token")
        self.stacked_widget.setCurrentWidget(self.loginUI)
        self.ui_loginUI.clear_inputs()
        print("Đã chuyển về loginUI và xóa nội dung ô nhập liệu")

    def check_login_status(self):
        settings = QSettings("MyApp", "LoginApp")
        token = settings.value("access_token", None)
        print(f"Token khi khởi động: {token}")
        print("Hiển thị loginUI, chờ người dùng đăng nhập")
        self.stacked_widget.setCurrentWidget(self.loginUI)

    def goINSIDE_to_loginUI(self):
        self.stacked_widget.setCurrentWidget(self.loginUI)

    def go_to_registerUI(self):
        self.stacked_widget.setCurrentWidget(self.registerUI)

    def go_to_forgot_passwordUI(self):
        self.stacked_widget.setCurrentWidget(self.forgotPasswordUI.enter_email_ui)

    def go_to_checkingUI(self):
        print("Chuyển sang checkingUI")
        self.stacked_widget.setCurrentWidget(self.checkingUI)
        settings = QSettings("MyApp", "LoginApp")
        token = settings.value("access_token", None)
        if token:
            print("Có token, gọi refresh_admin_info cho checkingUI")
            self.checkingUI.ui.header.refresh_admin_info()
        else:
            print("Không có token, không gọi refresh_admin_info")

    def go_to_checkingUI_2(self):
        print("Bắt đầu go_to_checkingUI_2")
        try:
            self.stacked_widget.setCurrentWidget(self.checkingUI_2)
            settings = QSettings("MyApp", "LoginApp")
            token = settings.value("access_token", None)
            print(f"Token trong go_to_checkingUI_2: {token}")
            if token:
                print("Có token, gọi refresh_admin_info")
                self.checkingUI_2.ui.header.refresh_admin_info()
                if not hasattr(self.checkingUI_2.ui.employee_row, 'all_employees') or not self.checkingUI_2.ui.employee_row.all_employees:
                    print("Chưa có danh sách nhân viên, gọi on_login_success")
                    self.checkingUI_2.on_login_success()
            else:
                print("Không có token, chuyển về loginUI")
                self.handle_logout()
            print("Kết thúc go_to_checkingUI_2")
        except Exception as e:
            print(f"Lỗi trong go_to_checkingUI_2: {str(e)}")
            QtWidgets.QMessageBox.critical(None, "Lỗi", f"Có lỗi xảy ra khi chuyển sang CheckingUI_2: {str(e)}")

    def go_to_informationUI(self):
        print("Chuyển sang informationUI")
        self.stacked_widget.setCurrentWidget(self.informationUI)
        settings = QSettings("MyApp", "LoginApp")
        token = settings.value("access_token", None)
        if token:
            print("Có token, gọi load_employees và refresh_admin_info")
            try:
                self.ui_informationUI.load_employees_from_api()
                self.ui_informationUI.header.refresh_admin_info()
            except Exception as e:
                print(f"Lỗi khi chuyển sang informationUI: {str(e)}")
                traceback.print_exc()
        else:
            print("Không có token, không gọi API")

    def open_otp_popup(self, email):
        if self.otp_popup is not None:
            self.otp_popup.close()
        self.otp_popup = OTPPopUp(email, is_for_registration=True)
        self.otp_popup.otp_verified.connect(self.on_otp_verified_for_registration)
        self.otp_popup.exec()

    def open_otp_popup_for_forgot_password(self, email):
        if self.otp_popup is not None:
            self.otp_popup.close()
        self.otp_popup = OTPPopUp(email, is_for_registration=False)
        self.otp_popup.otp_verified.connect(self.on_otp_verified_for_forgot_password)
        self.otp_popup.exec()

    def on_otp_verified_for_registration(self):
        print("OTP xác thực thành công cho đăng ký")
        QtWidgets.QMessageBox.information(self, "Thành công", "Đăng ký thành công! Vui lòng đăng nhập.")
        self.stacked_widget.setCurrentWidget(self.loginUI)
        self.ui_loginUI.clear_inputs()

    def on_otp_verified_for_forgot_password(self, email):
        print("OTP xác thực thành công cho quên mật khẩu")
        self.forgotPasswordUI.show_reset_password(email, self.otp_popup.get_otp_code())
        # Thay thế placeholder bằng reset_password_ui thực sự
        self.stacked_widget.removeWidget(self.reset_password_placeholder)
        self.stacked_widget.addWidget(self.forgotPasswordUI.reset_password_ui)
        self.forgotPasswordUI.reset_password_ui.password_reset_success.connect(self.goINSIDE_to_loginUI)
        self.stacked_widget.setCurrentWidget(self.forgotPasswordUI.reset_password_ui)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())