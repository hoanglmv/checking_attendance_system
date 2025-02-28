from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_loginUI(object):
    def setupUi(self, loginUI):
        loginUI.setObjectName("loginUI")
        loginUI.resize(750, 574)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(loginUI.sizePolicy().hasHeightForWidth())
        loginUI.setSizePolicy(sizePolicy)
        loginUI.setWindowOpacity(1.0)
        loginUI.setStyleSheet("background-color: #131A2D;")
        self.centralwidget = QtWidgets.QWidget(parent=loginUI)
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
        self.groupBox_2.setMinimumSize(QtCore.QSize(550, 420))
        self.groupBox_2.setMaximumSize(QtCore.QSize(550, 420))
        self.groupBox_2.setStyleSheet("background-color: #517078;\n"
                                       "border-radius: 3px;\n"
                                       "")
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.label = QtWidgets.QLabel(parent=self.groupBox_2)
        self.label.setGeometry(QtCore.QRect(220, 40, 111, 51))
        self.label.setStyleSheet("color: white;\n"
                                 "font: 18pt \"Times New Roman\";")
        self.label.setObjectName("label")
        self.user_name = QtWidgets.QLineEdit(parent=self.groupBox_2)
        self.user_name.setGeometry(QtCore.QRect(100, 109, 351, 31))
        self.user_name.setStyleSheet("border: none;\n"
                                      "border-bottom: 2px solid white;\n"
                                      "color: white;\n"
                                      "")
        self.user_name.setObjectName("user_name")
        self.password = QtWidgets.QLineEdit(parent=self.groupBox_2)
        self.password.setGeometry(QtCore.QRect(100, 159, 351, 31))
        self.password.setStyleSheet("border: none;\n"
                                     "border-bottom: 2px solid white;\n"
                                     "color: white;\n"
                                     "")
        self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)  
        self.password.setObjectName("password")
        self.login_button = QtWidgets.QPushButton(parent=self.groupBox_2)
        self.login_button.setGeometry(QtCore.QRect(100, 232, 351, 31))
        self.login_button.setStyleSheet("border: 2px solid white;\n"
                                         "color: white;\n"
                                         "font: 12pt \"Times New Roman\";")
        self.login_button.setObjectName("login_button")
        self.register_button = QtWidgets.QPushButton(parent=self.groupBox_2)
        self.register_button.setGeometry(QtCore.QRect(110, 290, 75, 23))
        self.register_button.setStyleSheet("color: white;\n"
                                            "font: 10pt \"Times New Roman\";")
        self.register_button.setObjectName("register_button")
        self.fogot_button = QtWidgets.QPushButton(parent=self.groupBox_2)
        self.fogot_button.setGeometry(QtCore.QRect(320, 290, 131, 23))
        self.fogot_button.setStyleSheet("color: white;\n"
                                         "font: 10pt \"Times New Roman\";")
        self.fogot_button.setObjectName("fogot_button")

        self.label_2 = QtWidgets.QLabel(parent=self.groupBox_2)
        self.label_2.setGeometry(QtCore.QRect(60, 110, 31, 31))
        self.label_2.setStyleSheet("padding-left: 30px;\n"
                                    "background-image: url(D:/NMCNPM/checking_attendance_system/fe/Image_and_icon/icons8-user-30.png); \n"
                                    "background-repeat: no-repeat;\n"
                                    "background-position: left center; ")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(parent=self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(60, 160, 31, 31))
        self.label_3.setStyleSheet("padding-left: 30px;\n"
                                    "background-image: url(D:/NMCNPM/checking_attendance_system/fe/Image_and_icon/icons8-password-30.png); \n"
                                    "background-repeat: no-repeat;\n"
                                    "background-position: left center; ")
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")

        self.eye = QtWidgets.QLabel(parent=self.groupBox_2)
        self.eye.setGeometry(QtCore.QRect(420, 165, 21, 21))
        self.eye.setStyleSheet("padding-left: 30px;\n"
                               "background-image: url(D:/NMCNPM/checking_attendance_system/fe/Image_and_icon/icons8-eye-20.png); \n"
                               "background-repeat: no-repeat;\n"
                               "background-position: left center; ")
        self.eye.setText("")
        self.eye.setObjectName("eye")
        
        self.blind = QtWidgets.QLabel(parent=self.groupBox_2)
        self.blind.setGeometry(QtCore.QRect(420, 165, 21, 21))
        self.blind.setStyleSheet("padding-left: 30px;\n"
                                 "background-image: url(D:/NMCNPM/checking_attendance_system/fe/Image_and_icon/icons8-blind-20.png); \n"
                                 "background-repeat: no-repeat;\n"
                                 "background-position: left center; ")
        self.blind.setText("")
        self.blind.setObjectName("blind")
        self.blind.hide() 
        self.horizontalLayout.addWidget(self.groupBox_2)
        spacerItem1 = QtWidgets.QSpacerItem(75, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        loginUI.setCentralWidget(self.centralwidget)

        self.retranslateUi(loginUI)
        QtCore.QMetaObject.connectSlotsByName(loginUI)

        self.eye.mousePressEvent = self.toggle_password_visibility
        self.blind.mousePressEvent = self.toggle_password_visibility

    def retranslateUi(self, loginUI):
        _translate = QtCore.QCoreApplication.translate
        loginUI.setWindowTitle(_translate("loginUI", "loginUI"))
        self.label.setText(_translate("loginUI", "Đăng nhập"))
        self.login_button.setText(_translate("loginUI", "Đăng nhập"))
        self.register_button.setText(_translate("loginUI", "Đăng kí"))
        self.fogot_button.setText(_translate("loginUI", "Quên mật khẩu"))

    def toggle_password_visibility(self, event):
        if self.password.echoMode() == QtWidgets.QLineEdit.EchoMode.Password:
            self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)  
            self.eye.hide()  
            self.blind.show()  
        else:
            self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
            self.eye.show()
            self.blind.hide()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    loginUI = QtWidgets.QMainWindow()
    ui = Ui_loginUI()
    ui.setupUi(loginUI)
    loginUI.show()
    sys.exit(app.exec())