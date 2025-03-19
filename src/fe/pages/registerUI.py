from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_registerUI(object):
    def setupUi(self, registerUI):
        registerUI.setObjectName("registerUI")
        registerUI.resize(750, 650)
        registerUI.setStyleSheet("background-color: #131A2D;")
        self.centralwidget = QtWidgets.QWidget(parent=registerUI)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        
        self.groupBox = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.groupBox.setStyleSheet("border: none;")
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        spacerItem = QtWidgets.QSpacerItem(198, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        
        self.groupBox_2 = QtWidgets.QGroupBox(parent=self.groupBox)
        self.groupBox_2.setMinimumSize(QtCore.QSize(550, 500))
        self.groupBox_2.setMaximumSize(QtCore.QSize(550, 500))
        self.groupBox_2.setStyleSheet("background-color: #517078;\n"
                                       "border-radius: 3px;")
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        
        self.label = QtWidgets.QLabel(parent=self.groupBox_2)
        self.label.setGeometry(QtCore.QRect(220, 30, 111, 51))
        self.label.setStyleSheet("color: white;\n"
                                 "font: 18pt \"Times New Roman\";")
        self.label.setObjectName("label")
        
        self.user_name = QtWidgets.QLineEdit(parent=self.groupBox_2)
        self.user_name.setGeometry(QtCore.QRect(100, 90, 351, 31))
        self.user_name.setStyleSheet("border: none;\n"
                                      "border-bottom: 2px solid white;\n"
                                      "color: white;")
        self.user_name.setObjectName("user_name")
        
        self.email = QtWidgets.QLineEdit(parent=self.groupBox_2)
        self.email.setGeometry(QtCore.QRect(100, 140, 351, 31))
        self.email.setStyleSheet("border: none;\n"
                                 "border-bottom: 2px solid white;\n"
                                 "color: white;")
        self.email.setObjectName("email")
        
        self.password = QtWidgets.QLineEdit(parent=self.groupBox_2)
        self.password.setGeometry(QtCore.QRect(100, 190, 351, 31))
        self.password.setStyleSheet("border: none;\n"
                                     "border-bottom: 2px solid white;\n"
                                     "color: white;")
        self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.password.setObjectName("password")
        
        self.confirm_password = QtWidgets.QLineEdit(parent=self.groupBox_2)
        self.confirm_password.setGeometry(QtCore.QRect(100, 240, 351, 31))
        self.confirm_password.setStyleSheet("border: none;\n"
                                            "border-bottom: 2px solid white;\n"
                                            "color: white;")
        self.confirm_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.confirm_password.setObjectName("confirm_password")
        
        self.register_button = QtWidgets.QPushButton(parent=self.groupBox_2)
        self.register_button.setGeometry(QtCore.QRect(100, 300, 351, 31))
        self.register_button.setStyleSheet("border: 2px solid white;\n"
                                           "color: white;\n"
                                           "font: 12pt \"Times New Roman\";")
        self.register_button.setObjectName("register_button")
        
        self.back_to_login = QtWidgets.QPushButton(parent=self.groupBox_2)
        self.back_to_login.setGeometry(QtCore.QRect(100, 350, 351, 31))
        self.back_to_login.setStyleSheet("color: white;\n"
                                         "font: 10pt \"Times New Roman\";")
        self.back_to_login.setObjectName("back_to_login")

        self.horizontalLayout.addWidget(self.groupBox_2)
        
        spacerItem1 = QtWidgets.QSpacerItem(75, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        
        registerUI.setCentralWidget(self.centralwidget)

        self.retranslateUi(registerUI)
        QtCore.QMetaObject.connectSlotsByName(registerUI)

    def retranslateUi(self, registerUI):
        _translate = QtCore.QCoreApplication.translate
        registerUI.setWindowTitle(_translate("registerUI", "Đăng ký"))
        self.label.setText(_translate("registerUI", "Đăng ký"))
        self.user_name.setPlaceholderText(_translate("registerUI", "Tên đăng nhập"))
        self.email.setPlaceholderText(_translate("registerUI", "Email"))
        self.password.setPlaceholderText(_translate("registerUI", "Mật khẩu"))
        self.confirm_password.setPlaceholderText(_translate("registerUI", "Nhập lại mật khẩu"))
        self.register_button.setText(_translate("registerUI", "Đăng ký"))
        self.back_to_login.setText(_translate("registerUI", "Quay lại đăng nhập"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    registerUI = QtWidgets.QMainWindow()
    ui = Ui_registerUI()
    ui.setupUi(registerUI)
    registerUI.show()
    sys.exit(app.exec())
