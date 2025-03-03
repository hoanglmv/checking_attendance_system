from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QWidget, QHeaderView, QAbstractItemView, QTableWidgetItem, QHBoxLayout, QCheckBox

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from fe.components.header import Header
from fe.components.sidebar import Sidebar

class Ui_checkingUI(object):
    def setupUi(self, checkingUI):
        checkingUI.setObjectName("checkingUI")
        checkingUI.resize(1560, 610)
        checkingUI.setStyleSheet("background-color: #0B121F; border: none;")
        
        self.centralwidget = QtWidgets.QWidget(parent=checkingUI)
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
        self.line_day.setStyleSheet("background-color: #9FEF00;\n"
"border-radius: 10px;")
        self.line_day.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_day.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_day.setObjectName("line_day")
        self.btn_day_attendance = QtWidgets.QPushButton(parent=self.splitter)
        self.btn_day_attendance.setMinimumSize(QtCore.QSize(150, 30))
        self.btn_day_attendance.setMaximumSize(QtCore.QSize(150, 30))
        self.btn_day_attendance.setStyleSheet("border: none;\n"
"font: 9pt \"Times New Roman\";\n"
"color: #9FEF00;")
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
        self.line_month.setStyleSheet("background-color: none;\n"
"border-radius: 10px;")
        self.line_month.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_month.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_month.setObjectName("line_month")
        self.btn_month_attendance = QtWidgets.QPushButton(parent=self.splitter_2)
        self.btn_month_attendance.setMinimumSize(QtCore.QSize(150, 30))
        self.btn_month_attendance.setMaximumSize(QtCore.QSize(150, 30))
        self.btn_month_attendance.setStyleSheet("border: none;\n"
"font: 9pt \"Times New Roman\";\n"
"color: #FFFFFF;\n"
"")
        self.btn_month_attendance.setText("Điểm danh theo tháng")
        self.btn_month_attendance.setObjectName("btn_month_attendance")
        self.verticalLayout.addWidget(self.groupBox)
        
        self.stas_time = QtWidgets.QGroupBox(parent=self.main)
        self.stas_time.setMinimumSize(QtCore.QSize(0, 75))
        self.stas_time.setMaximumSize(QtCore.QSize(16777215, 75))
        self.stas_time.setStyleSheet("background-color: #192E44;")
        self.stas_time.setTitle("")
        self.stas_time.setObjectName("stas_time")
        self.verticalLayout.addWidget(self.stas_time)
        
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.stas_time)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        
        self.horizontalLayout_2.addSpacing(20)
        
        self.btn_time = QtWidgets.QPushButton(parent=self.stas_time)
        self.btn_time.setMinimumSize(QtCore.QSize(200, 30))
        self.btn_time.setMaximumSize(QtCore.QSize(200, 30))
        self.btn_time.setStyleSheet("border: 2px solid white;\n"
"border-radius:5px;\n"
"color: white;\n"
"font: 9pt \"Times New Roman\";")
        self.btn_time.setText("Thứ 6, ngày 21/2/2025")
        self.btn_time.setObjectName("btn_time")
        self.horizontalLayout_2.addWidget(self.btn_time)
        
        self.horizontalLayout_2.addStretch()
        
        btn_total = self.create_btn(self.stas_time, "Tất cả", 40)
        btn_total.setObjectName("btn_total")
        self.horizontalLayout_2.addWidget(btn_total)

        self.horizontalLayout_2.addSpacing(10)
        
        btn_cm = self.create_btn(self.stas_time, "Có mặt", 37)
        btn_cm.setObjectName("btn_cm")
        self.horizontalLayout_2.addWidget(btn_cm)
        
        self.horizontalLayout_2.addSpacing(10)
        
        btn_cp = self.create_btn(self.stas_time, "Có phép", 2)
        btn_cp.setObjectName("btn_cp")
        self.horizontalLayout_2.addWidget(btn_cp)
        
        self.horizontalLayout_2.addSpacing(10)
        
        btn_kp = self.create_btn(self.stas_time, "Không phép", 1)
        btn_kp.setObjectName("btn_kp")
        self.horizontalLayout_2.addWidget(btn_kp)
        
        self.horizontalLayout_2.addSpacing(20)
         
        self.content = QtWidgets.QGroupBox(parent=self.main)
        self.content.setStyleSheet("")
        self.content.setTitle("")
        self.content.setObjectName("content")
        
        # Tạo bảng
        self.table = QtWidgets.QTableWidget(self.content)
        self.table.setColumnCount(8) 
        self.table.setHorizontalHeaderLabels(["ID", "Họ và tên", "Chức vụ", "Có mặt", "Giờ đến", "Giờ về", "Nghỉ có phép", "Nghỉ không phép"])

        self.table.setColumnWidth(0, 50)   
        self.table.setColumnWidth(2, 100) 
        self.table.setColumnWidth(3, 100) 
        self.table.setColumnWidth(4, 100) 
        self.table.setColumnWidth(5, 100) 
        self.table.setColumnWidth(6, 100) 
        self.table.setColumnWidth(7, 120) 
        # Kích thước tùy chỉnh
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

        # Cố định kích thước các cột ID và Số điện thoại
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeMode.Fixed)

        self.table.setStyleSheet("""
        QTableWidget {
                gridline-color: white; 
                border: 2px solid white; 
                color: white; 
        }                         
        QHeaderView::section {
                background-color: #192E44;
                color: white;             
                font-weight: bold;    
                padding: 5px;
                border: 1px solid white;
        }
        QTableWidget::item {
                background-color: #192E44;
                color: white;
                padding: 5px;
                border: 1px solid white;
        }
        """)
        
        self.table.horizontalHeader().setVisible(True)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.verticalHeader().setVisible(False)

        layout = QtWidgets.QVBoxLayout(self.content)
        layout.addWidget(self.table)
        self.content.setLayout(layout)
        
        # Dữ liệu người dùng
        self.add_row("001", "Cao Lê Phụng", "Nhân viên", True, "8.00", "17.00", False, False)
        self.add_row("002", "Cao Lê Phụng", "Nhân viên", False, "8.00", "17.00", True, False)
        self.add_row("001", "Cao Lê Phụng", "Nhân viên", False, "8.00", "17.00", False, True)

        self.verticalLayout.addWidget(self.content)

        self.horizontalLayout.addWidget(self.main)
        
        checkingUI.setCentralWidget(self.centralwidget)
    
    def retranslateUi(self, checkingUI):
        _translate = QtCore.QCoreApplication.translate
        checkingUI.setWindowTitle(_translate("checkingUI", "MainWindow"))
        
    def create_btn(self, pr, status, count):
        button = QtWidgets.QPushButton(parent = pr)
        button.setMinimumSize(QtCore.QSize(100, 30))
        button.setMaximumSize(QtCore.QSize(100, 30))        
        button.setStyleSheet("border: 2px solid white;\n"
"border-radius:5px;\n"
"color: white;\n"
"font: 9pt \"Times New Roman\";")
        button.setText(f"{status}: {count}")
        return button

    def add_row(self, id, name, role, check, time_in, time_out, cp, kp):
        row_count = self.table.rowCount()
        self.table.setRowCount(row_count + 1) 

        self.table.setItem(row_count, 0, QTableWidgetItem(id))
        self.table.setItem(row_count, 1, QTableWidgetItem(name))
        self.table.setItem(row_count, 2, QTableWidgetItem(role))
        self.table.setItem(row_count, 4, QTableWidgetItem(time_in))
        self.table.setItem(row_count, 5, QTableWidgetItem(time_out))
        self.table.setItem(row_count, 6, QTableWidgetItem(cp))
        self.table.setItem(row_count, 7, QTableWidgetItem(kp))

        checkbox_widget = QWidget()
        checkbox_layout = QHBoxLayout(checkbox_widget)
        checkbox_layout.setContentsMargins(0, 0, 0, 0) 
        checkbox = QCheckBox()
        checkbox_layout.addWidget(checkbox)
        checkbox_layout.setAlignment(checkbox, QtCore.Qt.AlignmentFlag.AlignCenter) 

        self.table.setCellWidget(row_count, 3, checkbox_widget)
        self.table.setCellWidget(row_count, 6, checkbox_widget)
        self.table.setCellWidget(row_count, 7, checkbox_widget)
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    checkingUI = QtWidgets.QMainWindow()
    ui = Ui_checkingUI()
    ui.setupUi(checkingUI)
    checkingUI.show()
    sys.exit(app.exec())
