from PyQt6 import QtCore, QtGui, QtWidgets
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from fe.components.header import Header
from fe.components.sidebar import Sidebar

class Ui_checkingUI(object):
    def setupUi(self, checkingUI):
        checkingUI.setObjectName("checkingUI")
        checkingUI.resize(1552, 607)
        checkingUI.setStyleSheet("background-color: #0B121F; border: none;")
        
        self.centralwidget = QtWidgets.QWidget(parent=checkingUI)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        
        self.groupBox = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setContentsMargins(1, 0, 1, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        # Sidebar
        self.sidebar = Sidebar(parent=self.groupBox)
        self.horizontalLayout.addWidget(self.sidebar)
        
        self.main = QtWidgets.QGroupBox(parent=self.groupBox)
        self.main.setStyleSheet("")
        self.main.setTitle("")
        self.main.setObjectName("main")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.main)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        
        # Header
        self.header = Header(parent=self.main)
        self.verticalLayout_2.addWidget(self.header)
        
        self.horizontalLayout.addWidget(self.main)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
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
