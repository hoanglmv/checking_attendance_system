from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QWidget, QHeaderView, QAbstractItemView, QTableWidgetItem, QHBoxLayout, QCheckBox
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
        self.line_day.setStyleSheet("background-color: none;\n"
"border-radius: 10px;")
        self.line_day.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_day.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_day.setObjectName("line_day")
        self.btn_day_attendance = QtWidgets.QPushButton(parent=self.splitter)
        self.btn_day_attendance.setMinimumSize(QtCore.QSize(150, 30))
        self.btn_day_attendance.setMaximumSize(QtCore.QSize(150, 30))
        self.btn_day_attendance.setStyleSheet("border: none;\n"
"font: 9pt \"Times New Roman\";\n"
"color: white;")
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
        self.line_month.setStyleSheet("background-color: #9FEF00;\n"
"border-radius: 10px;")
        self.line_month.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_month.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_month.setObjectName("line_month")
        self.btn_month_attendance = QtWidgets.QPushButton(parent=self.splitter_2)
        self.btn_month_attendance.setMinimumSize(QtCore.QSize(150, 30))
        self.btn_month_attendance.setMaximumSize(QtCore.QSize(150, 30))
        self.btn_month_attendance.setStyleSheet("border: none;\n"
"font: 9pt \"Times New Roman\";\n"
"color: #9FEF00;\n"
"")
        self.btn_month_attendance.setText("Điểm danh theo tháng")
        self.btn_month_attendance.setObjectName("btn_month_attendance")
        self.verticalLayout.addWidget(self.groupBox)
        
        self.employee_row = QtWidgets.QGroupBox(parent=self.main)
        self.employee_row.setMinimumSize(QtCore.QSize(0, 150))
        self.employee_row.setMaximumSize(QtCore.QSize(16777215, 150))
        self.employee_row.setStyleSheet("background-color: #192E44;\n margin-bottom: 5px")
        self.employee_row.setTitle("")
        self.employee_row.setObjectName("employee_row")
        self.verticalLayout.addWidget(self.employee_row)
        
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.employee_row)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        
        # self.horizontalLayout_2.addCard
         
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
        
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.content_header)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.horizontalLayout_2.addSpacing(30)
        
        self.pushButton = QtWidgets.QPushButton(parent=self.content_header)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setStyleSheet("border: none; color: white; font: 12pt 'Times New Roman';")
        self.pushButton.setText("12345 - Cao Lê Phụng")
        self.horizontalLayout_2.addWidget(self.pushButton)
        
        self.horizontalLayout_2.addStretch()
        
        self.tooltip_kp = self.tooltip(self.content_header, "#EEBE3C", "Không phép")
        self.horizontalLayout_2.addWidget(self.tooltip_kp)
        
        self.horizontalLayout_2.addSpacing(10)
        
        self.tooltip_cp = self.tooltip(self.content_header, "#2A4CFA", "Có phép")
        self.horizontalLayout_2.addWidget(self.tooltip_cp)
        
        self.horizontalLayout_2.addSpacing(10)
        
        self.tooltip_tg = self.tooltip(self.content_header, "#33D64B", "Thiếu giờ")
        self.horizontalLayout_2.addWidget(self.tooltip_tg)
        
        self.horizontalLayout_2.addSpacing(10)
        
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
        
    def tooltip(self, pr, color, text):
        container = QtWidgets.QWidget(parent = pr)
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
    checkingUI_2.show()
    sys.exit(app.exec())
