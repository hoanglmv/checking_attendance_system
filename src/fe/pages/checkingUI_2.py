from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QWidget, QHeaderView, QAbstractItemView, QTableWidgetItem, QHBoxLayout, QCheckBox, QListWidget, QListWidgetItem, QLabel
from PyQt6.QtGui import QIcon, QTextCharFormat, QBrush, QPen, QColor
from PyQt6.QtCore import QDate, Qt

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from fe.components.header import Header
from fe.components.sidebar import Sidebar

class Ui_checkingUI_2(object):
    def setupUi(self, checkingUI_2):
        checkingUI_2.setObjectName("checkingUI_2")
        checkingUI_2.resize(1560, 610)
        checkingUI_2.setStyleSheet("background-color: #0B121F; border: none;")
        
        self.centralwidget = QtWidgets.QWidget(parent=checkingUI_2)
        self.centralwidget.setObjectName("centralwidget")
        
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        
        self.sidebar = Sidebar(parent=self.centralwidget)
        self.sidebar.fil_attendance.setStyleSheet("background-color: #68D477; \n border-radius: 5px;")
        self.horizontalLayout.addWidget(self.sidebar)       
       
        self.main = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.main.setObjectName("main")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.main)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)   
        
        self.header = Header(parent=self.main)
        self.verticalLayout.addWidget(self.header)     
        
        self.groupBox = QtWidgets.QGroupBox(parent=self.main)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 60))
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 60))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.splitter = QtWidgets.QSplitter(parent=self.groupBox)
        self.splitter.setGeometry(QtCore.QRect(10, 0, 150, 35))
        self.splitter.setMinimumSize(QtCore.QSize(150, 35))
        self.splitter.setMaximumSize(QtCore.QSize(150, 35))
        self.splitter.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.splitter.setObjectName("splitter")
        self.line_day = QtWidgets.QFrame(parent=self.splitter)
        self.line_day.setMinimumSize(QtCore.QSize(150, 4))
        self.line_day.setMaximumSize(QtCore.QSize(150, 4))
        self.line_day.setStyleSheet("background-color: none;\nborder-radius: 10px;")
        self.line_day.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_day.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_day.setObjectName("line_day")
        self.btn_day_attendance = QtWidgets.QPushButton(parent=self.splitter)
        self.btn_day_attendance.setMinimumSize(QtCore.QSize(150, 30))
        self.btn_day_attendance.setMaximumSize(QtCore.QSize(150, 30))
        self.btn_day_attendance.setStyleSheet("border: none;\nfont: 9pt \"Times New Roman\";\ncolor: white;")
        self.btn_day_attendance.setText("Điểm danh theo ngày")
        self.btn_day_attendance.setObjectName("btn_day_attendance")
        
        self.splitter_2 = QtWidgets.QSplitter(parent=self.groupBox)
        self.splitter_2.setGeometry(QtCore.QRect(170, 0, 150, 35))
        self.splitter_2.setMinimumSize(QtCore.QSize(150, 35))
        self.splitter_2.setMaximumSize(QtCore.QSize(150, 35))
        self.splitter_2.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.splitter_2.setObjectName("splitter_2")
        self.line_month = QtWidgets.QFrame(parent=self.splitter_2)
        self.line_month.setMinimumSize(QtCore.QSize(150, 4))
        self.line_month.setMaximumSize(QtCore.QSize(150, 4))
        self.line_month.setStyleSheet("background-color: #9FEF00;\nborder-radius: 10px;")
        self.line_month.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_month.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_month.setObjectName("line_month")
        self.btn_month_attendance = QtWidgets.QPushButton(parent=self.splitter_2)
        self.btn_month_attendance.setMinimumSize(QtCore.QSize(150, 30))
        self.btn_month_attendance.setMaximumSize(QtCore.QSize(150, 30))
        self.btn_month_attendance.setStyleSheet("border: none;\nfont: 9pt \"Times New Roman\";\ncolor: #9FEF00;")
        self.btn_month_attendance.setText("Điểm danh theo tháng")
        self.btn_month_attendance.setObjectName("btn_month_attendance")
        self.verticalLayout.addWidget(self.groupBox)
        
        # Employee row - hiển thị danh sách card nhân viên theo hàng ngang
        self.employee_row = QtWidgets.QGroupBox(parent=self.main)
        self.employee_row.setMinimumSize(QtCore.QSize(0, 150))
        self.employee_row.setMaximumSize(QtCore.QSize(1300, 150))
        self.employee_row.setStyleSheet("margin-bottom: 2px;")
        self.employee_row.setTitle("")
        self.employee_row.setObjectName("employee_row")
        self.verticalLayout.addWidget(self.employee_row)
        
        # Layout riêng cho employee_row
        self.employeeLayout = QtWidgets.QHBoxLayout(self.employee_row)
        self.employeeLayout.setObjectName("employeeLayout")
        
        # Tạo QListWidget hiển thị theo hàng ngang
        self.employeeList = QtWidgets.QListWidget(self.employee_row)
        self.employeeList.setStyleSheet("""
            QListWidget {
                background-color: #0B121F;
                border-top: 2px solid white;
            }
            QListWidget::item {
                background-color: #192E44;
                border: 1px solid #5A6986;
                border-radius: 8px;
                padding: 2px;
                margin: 5px;
                color: white;
                font-size: 8px;
            }
            QListWidget::item:selected {
                border: 2px solid #9FEF00;
                background-color: #0F2A47;
            }
        """)
        self.employeeList.setFixedHeight(150)
        self.employeeList.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.employeeList.setViewMode(QtWidgets.QListView.ViewMode.IconMode)
        self.employeeList.setFlow(QtWidgets.QListView.Flow.LeftToRight)
        self.employeeList.setWrapping(False)  # Không xuống dòng, hiển thị theo hàng ngang
        self.employeeList.setFixedHeight(200)   # Chiều cao phù hợp với employee_row
        
        # Kết nối sự kiện click vào item
        self.employeeLayout.addWidget(self.employeeList)
        
        # Phần nội dung chính phía dưới (content)
        self.content = QtWidgets.QGroupBox(parent=self.main)
        self.content.setTitle("")
        self.content.setObjectName("content")
        
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.content)
        self.content.setStyleSheet("background-color:#192E44;")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        
        self.content_header = QtWidgets.QGroupBox(parent=self.content)
        self.content_header.setMinimumSize(QtCore.QSize(0, 60))
        self.content_header.setMaximumSize(QtCore.QSize(16777215, 60))
        self.content_header.setStyleSheet("border-bottom: 1px solid white;")
        self.content_header.setTitle("")
        self.content_header.setObjectName("content_header")
        
        # Layout riêng cho content_header
        self.contentHeaderLayout = QtWidgets.QHBoxLayout(self.content_header)
        self.contentHeaderLayout.setObjectName("contentHeaderLayout")
        self.contentHeaderLayout.addSpacing(30)
        
        self.pushButton = QtWidgets.QPushButton(parent=self.content_header)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setStyleSheet("border: none; color: white; font: 12pt 'Times New Roman';")
        self.pushButton.setText("12345 - Cao Lê Phụng")
        self.contentHeaderLayout.addWidget(self.pushButton)
        
        self.contentHeaderLayout.addStretch()
        
        self.tooltip_kp = self.tooltip(self.content_header, "#EEBE3C", "Không phép")
        self.contentHeaderLayout.addWidget(self.tooltip_kp)
        self.contentHeaderLayout.addSpacing(10)
        
        self.tooltip_cp = self.tooltip(self.content_header, "#2A4CFA", "Có phép")
        self.contentHeaderLayout.addWidget(self.tooltip_cp)
        self.contentHeaderLayout.addSpacing(10)
        
        self.tooltip_tg = self.tooltip(self.content_header, "#33D64B", "Thiếu giờ")
        self.contentHeaderLayout.addWidget(self.tooltip_tg)
        self.contentHeaderLayout.addSpacing(10)
        
        self.verticalLayout_2.addWidget(self.content_header)
        
        self.content_calendar = QtWidgets.QGroupBox(parent=self.content)
        self.content_calendar.setStyleSheet("")
        self.content_calendar.setTitle("")
        self.content_calendar.setObjectName("content_calendar")
        
        self.calendar = QtWidgets.QCalendarWidget(parent=self.content_calendar)
        self.calendar.setGridVisible(True)
        self.calendar.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
        self.calendar.setStyleSheet("""
        QCalendarWidget QWidget {
                alternate-background-color: #2C3E50;
                color: white;
        }
        QCalendarWidget QToolButton {
                color: white;
                font-size: 14px;
                font-weight: bold;
                background-color: #34495E;
                padding: 10px;
        }
        QCalendarWidget QToolButton::icon {
                width: 25px;
                height: 25px;
        }
        QCalendarWidget QHeaderView {
                background-color: #9FEF00;
                color: white;
                font-weight: bold;
                font-size: 16px;
        }
        QCalendarWidget QTableView {
                selection-background-color: #68D477;
                color: white;
                font-size: 14px;
                gridline-color: #34495E;
        }
        """)
        self.highlight_date(QDate(2025, 3, 10), "#EEBE3C")
        self.highlight_date(QDate(2025, 3, 22), "#2A4CFA")
        self.highlight_date(QDate(2025, 3, 18), "#33D64B")
 
        self.calendar.setMinimumSize(QtCore.QSize(400, 300))  
        self.verticalLayout_2.addWidget(self.calendar)

        self.verticalLayout_2.addWidget(self.content_calendar)
        
        self.verticalLayout.addWidget(self.content)

        self.horizontalLayout.addWidget(self.main)
        
        checkingUI_2.setCentralWidget(self.centralwidget)
        
    def retranslateUi(self, checkingUI_2):
        _translate = QtCore.QCoreApplication.translate
        checkingUI_2.setWindowTitle(_translate("checkingUI_2", "MainWindow"))
        
    def highlight_date(self, date, color):
        fmt = QTextCharFormat()
        if isinstance(color, str):
            color = QColor(color)
        fmt.setBackground(QBrush(color))
        self.calendar.setDateTextFormat(date, fmt)

    def add_employee_to_list(self, emp):
        """
        Tạo widget cho một nhân viên và thêm vào QListWidget.
        Dữ liệu emp là dictionary chứa các thông tin: id, name, position, office.
        """
        item = QListWidgetItem()
        itemWidget = QWidget()
        layout = QHBoxLayout(itemWidget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(50)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        photoLabel = QLabel()
        photoLabel.setFixedSize(80, 80)
        photoLabel.setStyleSheet("border-radius: 30px; border: 2px solid white;")
        
        info_text = (
            f"ID: {emp.get('id', '')}\n"
            f"Họ tên: {emp.get('name', '')}\n"
            f"Chức vụ: {emp.get('position', '')}\n"
            f"Nơi làm việc: {emp.get('office', '')}"
        )
        info = QLabel(info_text)
        info.setStyleSheet("color: white; font-size: 14px;")
        
        layout.addWidget(photoLabel)
        layout.addWidget(info)
        itemWidget.setLayout(layout)
        
        item.setSizeHint(itemWidget.sizeHint() + QtCore.QSize(50, 30))
        self.employeeList.addItem(item)
        self.employeeList.setItemWidget(item, itemWidget)
        item.setData(Qt.ItemDataRole.UserRole, emp)

    def tooltip(self, pr, color, text):
        container = QtWidgets.QWidget(parent=pr)
        container.setStyleSheet("background: transparent;")  
        layout = QtWidgets.QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        icon_button = QtWidgets.QPushButton(container)
        icon_button.setMinimumSize(QtCore.QSize(30, 37))
        icon_button.setMaximumSize(QtCore.QSize(30, 37))
        icon_button.setStyleSheet(
            f"border: none; background-color: {color}; background-repeat: no-repeat; background-position: center center;"
            "border-radius: 5px;"
        )

        text_button = QtWidgets.QPushButton(text, container)
        text_button.setMinimumSize(QtCore.QSize(150, 37))
        text_button.setMaximumSize(QtCore.QSize(150, 37))
        text_button.setStyleSheet("border: none; color: white; font: 12pt 'Times New Roman';")
        
        layout.addWidget(icon_button)
        layout.addWidget(text_button)
        return container

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    checkingUI_2 = QtWidgets.QMainWindow()
    ui = Ui_checkingUI_2()
    ui.setupUi(checkingUI_2)
    ui.retranslateUi(checkingUI_2)
    # Ví dụ: thêm nhân viên mẫu
    ui.add_employee_to_list({"id": "2004", "name": "Lê Đoàn T", "position": "Nhân viên", "office": "Phòng 301"})
    ui.add_employee_to_list({"id": "20043", "name": "Nguyễn Hữu T", "position": "Nhân viên", "office": "Phòng 302"})
    ui.add_employee_to_list({"id": "2004", "name": "Lê Đoàn T", "position": "Nhân viên", "office": "Phòng 301"})
    ui.add_employee_to_list({"id": "20043", "name": "Nguyễn Hữu T", "position": "Nhân viên", "office": "Phòng 302"})
    ui.add_employee_to_list({"id": "2004", "name": "Lê Đoàn T", "position": "Nhân viên", "office": "Phòng 301"})
    ui.add_employee_to_list({"id": "20043", "name": "Nguyễn Hữu T", "position": "Nhân viên", "office": "Phòng 302"})
    ui.add_employee_to_list({"id": "2004", "name": "Lê Đoàn T", "position": "Nhân viên", "office": "Phòng 301"})
    ui.add_employee_to_list({"id": "20043", "name": "Nguyễn Hữu T", "position": "Nhân viên", "office": "Phòng 302"})
    checkingUI_2.show()
    sys.exit(app.exec())
