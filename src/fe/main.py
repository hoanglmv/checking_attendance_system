from PyQt6 import QtWidgets
from pages.loginUI import Ui_loginUI
from pages.checkingUI import Ui_checkingUI
from pages.notificationPopup import NotificationPopup  
from pages.adminPopup import AdminInfoPopup  

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Tạo QStackedWidget
        self.setWindowTitle("Checking Attendance System")
        self.setGeometry(100, 100, 800, 600)

        self.stacked_widget = QtWidgets.QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        # Tạo các trang
        self.loginUI = QtWidgets.QMainWindow()
        self.ui_loginUI = Ui_loginUI()
        self.ui_loginUI.setupUi(self.loginUI)
        self.stacked_widget.addWidget(self.loginUI)

        self.checkingUI = QtWidgets.QMainWindow()
        self.ui_checkingUI = Ui_checkingUI()
        self.ui_checkingUI.setupUi(self.checkingUI)
        self.stacked_widget.addWidget(self.checkingUI)

        # Kết nối nút nhấn
        self.ui_loginUI.login_button.clicked.connect(self.go_to_checkingUI)
        self.ui_checkingUI.sidebar.btn_logout.clicked.connect(self.go_to_loginUI)
        self.ui_checkingUI.header.buttons["bell"].clicked.connect(self.show_notification)
        self.ui_checkingUI.header.btn_admin.clicked.connect(self.show_admin)

        # Hiển thị trang đầu tiên
        self.stacked_widget.setCurrentWidget(self.loginUI)

    def go_to_loginUI(self):
        self.stacked_widget.setCurrentWidget(self.loginUI)

    def go_to_checkingUI(self):
        self.stacked_widget.setCurrentWidget(self.checkingUI)

    def show_notification(self):
        self.notification_popup = NotificationPopup(self)
        bell_button = self.ui_checkingUI.header.buttons["bell"]
        self.notification_popup.show_near(bell_button)

    def show_admin(self):
        self.admin_popup = AdminInfoPopup(self)
        admin_button = self.ui_checkingUI.header.btn_admin
        self.admin_popup.show_near(admin_button)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())