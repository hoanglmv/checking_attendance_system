from PyQt6 import QtCore, QtGui, QtWidgets
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
         
        self.content = QtWidgets.QGroupBox(parent=self.main)
        self.content.setStyleSheet("")
        self.content.setTitle("")
        self.content.setObjectName("content")
        self.verticalLayout.addWidget(self.content)

        self.horizontalLayout.addWidget(self.main)
        
        checkingUI.setCentralWidget(self.centralwidget)
    
    def retranslateUi(self, checkingUI):
        _translate = QtCore.QCoreApplication.translate
        checkingUI.setWindowTitle(_translate("checkingUI", "MainWindow"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    checkingUI = QtWidgets.QMainWindow()
    ui = Ui_checkingUI()
    ui.setupUi(checkingUI)
    checkingUI.show()
    sys.exit(app.exec())
