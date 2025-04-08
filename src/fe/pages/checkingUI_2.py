from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtCore import pyqtSignal
from pages.listChecking_2 import ListChecking_2
from pages.attendance_calendar import AttendanceCalendar
from components.sidebar import Sidebar
from components.header import Header
import logging

# Cấu hình logging
logging.basicConfig(
    filename='app.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Ui_checkingUI_2(object):
    def setupUi(self, checkingUI_2):
        logging.info("Bắt đầu setupUi trong Ui_checkingUI_2")
        checkingUI_2.setObjectName("checkingUI_2")
        checkingUI_2.setMinimumSize(QtCore.QSize(800, 600))
        checkingUI_2.setStyleSheet("background-color: #0B121F; border: none;")

        self.centralwidget = QtWidgets.QWidget(parent=checkingUI_2)
        self.centralwidget.setObjectName("centralwidget")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0,0,0,0)
        self.horizontalLayout.setSpacing(0)

        # Sử dụng Sidebar từ components
        self.sidebar = Sidebar(parent=self.centralwidget)
        self.sidebar.fil_attendance.setStyleSheet("background-color: #68D477; \n border-radius: 5px;")
        self.sidebar.fil_manage.setStyleSheet("background-color: #1B2B40; border-radius: 5px;")
        self.horizontalLayout.addWidget(self.sidebar)

        # Main content area
        self.main = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.main.setObjectName("main")
        self.main.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.main)
        self.verticalLayout.setContentsMargins(0,0,0,0)
        self.verticalLayout.setSpacing(0)

        # Sử dụng Header từ components
        self.header = Header(parent=self.main)
        self.header.header_title.setText("Điểm danh")
        self.verticalLayout.addWidget(self.header)

        # Buttons (Day/Month Attendance)
        self.groupBox = QtWidgets.QGroupBox(parent=self.main)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 50))
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 50))
        self.groupBox.setTitle("")
        self.button_layout = QtWidgets.QHBoxLayout(self.groupBox)
        self.button_layout.setContentsMargins(10, 10, 10, 10)
        self.button_layout.setSpacing(10)

        self.btn_day_attendance = QtWidgets.QPushButton(parent=self.groupBox)
        self.btn_day_attendance.setMinimumSize(QtCore.QSize(180, 40))
        self.btn_day_attendance.setMaximumSize(QtCore.QSize(180, 40))
        self.btn_day_attendance.setStyleSheet("""
            QPushButton {
                background: #1E2A38;
                color: #C0C0C0;
                padding: 8px 16px;
                border-radius: 6px;
                font-size: 12px;
                font-weight: 600;
                transition: all 0.3s ease;
            }
            QPushButton:hover {
                background: #2E3A4E;
                color: #A4F9C8;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
                transform: scale(1.05);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #68D477, stop:1 #4CAF50);
                color: black;
                border-bottom: 2px solid #4CAF50;
            }
        """)
        self.btn_day_attendance.setText("Điểm danh theo ngày")
        self.btn_day_attendance.setObjectName("btn_day_attendance")
        self.btn_day_attendance.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.button_layout.addWidget(self.btn_day_attendance)

        self.btn_month_attendance = QtWidgets.QPushButton(parent=self.groupBox)
        self.btn_month_attendance.setMinimumSize(QtCore.QSize(180, 40))
        self.btn_month_attendance.setMaximumSize(QtCore.QSize(180, 40))
        self.btn_month_attendance.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #68D477, stop:1 #4CAF50);
                color: black;
                padding: 8px 16px;
                border-radius: 6px;
                font-size: 12px;
                font-weight: 600;
                border-bottom: 2px solid #4CAF50;
                transition: all 0.3s ease;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #7BEF88, stop:1 #5CBF60);
                color: black;
                box-shadow: 0 2px 4px rgba(104, 212, 119, 0.5);
                transform: scale(1.05);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #68D477, stop:1 #4CAF50);
                color: black;
                border-bottom: 2px solid #4CAF50;
            }
        """)
        self.btn_month_attendance.setText("Điểm danh theo tháng")
        self.btn_month_attendance.setObjectName("btn_month_attendance")
        self.btn_month_attendance.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.button_layout.addWidget(self.btn_month_attendance)

        self.button_layout.addStretch()
        self.verticalLayout.addWidget(self.groupBox)

        # Employee List
        self.employee_row = ListChecking_2(parent=self.main)
        self.verticalLayout.addWidget(self.employee_row)

        # Attendance Calendar
        self.content = AttendanceCalendar(parent=self.main)
        self.content.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding))
        self.verticalLayout.addWidget(self.content)

        # Kết nối tín hiệu sau khi self.content đã được khởi tạo
        self.employee_row.employeeList.itemClicked.connect(self.content.on_employee_clicked)

        self.horizontalLayout.addWidget(self.main)
        self.horizontalLayout.setStretch(0, 1)  # Sidebar
        self.horizontalLayout.setStretch(1, 4)  # Main content

        checkingUI_2.setCentralWidget(self.centralwidget)
        logging.info("Hoàn tất setupUi trong Ui_checkingUI_2")

    def load_employees(self):
        self.employee_row.load_employees()

class CheckingUI_2(QtWidgets.QMainWindow):
    switch_to_day_signal = pyqtSignal()
    switch_to_month_signal = pyqtSignal()
    logout_signal = pyqtSignal()

    def __init__(self, stacked_widget=None):
        super().__init__()
        logging.info("Khởi tạo CheckingUI_2")
        self.stacked_widget = stacked_widget
        self.ui = Ui_checkingUI_2()
        self.ui.setupUi(self)

        self.ui.btn_day_attendance.clicked.connect(self.switch_to_day_signal.emit)
        self.ui.btn_month_attendance.clicked.connect(self.switch_to_month_signal.emit)
        logging.info("Đã kết nối tín hiệu trong CheckingUI_2")

    def on_login_success(self):
        logging.info("CheckingUI_2 nhận tín hiệu đăng nhập thành công")
        self.ui.load_employees()