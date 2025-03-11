from PyQt6 import QtWidgets
from pages.loginUI import Ui_loginUI
from pages.checkingUI import Ui_checkingUI
from pages.checkingUI_2 import Ui_checkingUI_2
from pages.informationUI import Ui_informationUI
from pages.notificationPopup import NotificationPopup  
from pages.adminPopup import AdminInfoPopup  
from pages.informationUI import Ui_informationUI

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

        # Tạo trang Checking
        self.checkingUI = QtWidgets.QMainWindow()
        self.ui_checkingUI = Ui_checkingUI()
        self.ui_checkingUI.setupUi(self.checkingUI)
        self.stacked_widget.addWidget(self.checkingUI)

        self.checkingUI_2 = QtWidgets.QMainWindow()
        self.ui_checkingUI_2 = Ui_checkingUI_2()
        self.ui_checkingUI_2.setupUi(self.checkingUI_2)
        self.stacked_widget.addWidget(self.checkingUI_2)

        self.informationUI = QtWidgets.QMainWindow()
        self.ui_informationUI = Ui_informationUI()
        self.ui_informationUI.setupUi(self.informationUI)
        self.stacked_widget.addWidget(self.informationUI)

        # Kết nối button loginUI (mượn tạm btn đăng nhập với quên mật khẩu)
        self.ui_loginUI.fogot_button.clicked.connect(self.go_to_checkingUI) 
        self.ui_loginUI.login_button.clicked.connect(self.go_to_checkingUI_2)
        
        # Kết nối button checkingUI
        self.ui_checkingUI.sidebar.btn_manage.clicked.connect(self.go_to_informationUI)
        self.ui_checkingUI.sidebar.btn_logout.clicked.connect(self.go_to_loginUI)
        
        self.ui_checkingUI.header.buttons["bell"].clicked.connect(self.show_notification)
        self.ui_checkingUI.header.btn_admin.clicked.connect(self.show_admin)
        
        self.ui_checkingUI.btn_month_attendance.clicked.connect(self.go_to_checkingUI_2)
        
        # Kết nối button checkingUI_2
        self.ui_checkingUI_2.sidebar.btn_manage.clicked.connect(self.go_to_informationUI)
        self.ui_checkingUI_2.sidebar.btn_logout.clicked.connect(self.go_to_loginUI)
        
        self.ui_checkingUI_2.header.buttons["bell"].clicked.connect(self.show_notification)
        self.ui_checkingUI_2.header.btn_admin.clicked.connect(self.show_admin)
        
        self.ui_checkingUI_2.btn_day_attendance.clicked.connect(self.go_to_checkingUI)
        
        # Kết nối button informationUI
        self.ui_informationUI.sidebar.btn_attendance.clicked.connect(self.go_to_checkingUI)
        self.ui_informationUI.sidebar.btn_logout.clicked.connect(self.go_to_loginUI)
        
        self.ui_informationUI.header.buttons["bell"].clicked.connect(self.show_notification)
        self.ui_informationUI.header.btn_admin.clicked.connect(self.show_admin)
        

        # Hiển thị trang đầu tiên
        self.stacked_widget.setCurrentWidget(self.loginUI)
        
    def current_page(self):
        return self.stacked_widget.currentWidget()

    def go_to_loginUI(self):
        self.stacked_widget.setCurrentWidget(self.loginUI)

    def go_to_informationUI(self):
        self.stacked_widget.setCurrentWidget(self.informationUI)

    def go_to_checkingUI(self):
        self.stacked_widget.setCurrentWidget(self.checkingUI)

    def go_to_checkingUI_2(self):
        self.stacked_widget.setCurrentWidget(self.checkingUI_2)

    def show_notification(self):
        self.notification_popup = NotificationPopup(self)
        self.position_popup(self.notification_popup)

    def show_admin(self):
        self.admin_popup = AdminInfoPopup(self)
        self.position_popup(self.admin_popup)

    def position_popup(self, popup):
        main_rect = self.geometry() 
        popup_rect = popup.geometry() 

        pos_x = main_rect.x() + main_rect.width() - popup_rect.width() - 30
        pos_y = main_rect.y() + 80

        popup.move(pos_x, pos_y) 
        popup.show() 



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())