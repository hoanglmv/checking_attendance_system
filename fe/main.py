from PyQt6 import QtWidgets
from loginUI import Ui_loginUI
from checkingUI import Ui_checkingUI

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
        self.ui_checkingUI.logout_button.clicked.connect(self.go_to_loginUI)

        # Hiển thị trang đầu tiên
        self.stacked_widget.setCurrentWidget(self.loginUI)

    def go_to_loginUI(self):
        self.stacked_widget.setCurrentWidget(self.loginUI)

    def go_to_checkingUI(self):
        self.stacked_widget.setCurrentWidget(self.checkingUI)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())