from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_ForgotPasswordUI(object):
    def setupUi(self, ForgotPasswordUI):
        ForgotPasswordUI.setObjectName("ForgotPasswordUI")
        ForgotPasswordUI.resize(750, 450)
        ForgotPasswordUI.setStyleSheet("background-color: #131A2D;")

        self.centralwidget = QtWidgets.QWidget(parent=ForgotPasswordUI)
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
        self.groupBox_2.setMinimumSize(QtCore.QSize(450, 350))
        self.groupBox_2.setMaximumSize(QtCore.QSize(450, 350))
        self.groupBox_2.setStyleSheet("background-color: #517078;\n"
                                       "border-radius: 3px;")
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")

        # Tiêu đề
        self.label = QtWidgets.QLabel(parent=self.groupBox_2)
        self.label.setGeometry(QtCore.QRect(140, 20, 200, 30))
        self.label.setStyleSheet("color: white;\n"
                                 "font: 18pt \"Times New Roman\";")
        self.label.setObjectName("label")

        # Trường nhập email
        self.email = QtWidgets.QLineEdit(parent=self.groupBox_2)
        self.email.setGeometry(QtCore.QRect(50, 70, 350, 31))
        self.email.setStyleSheet("border: none;\n"
                                 "border-bottom: 2px solid white;\n"
                                 "color: white;")
        self.email.setObjectName("email")

        # Trường nhập mật khẩu mới
        self.new_password = QtWidgets.QLineEdit(parent=self.groupBox_2)
        self.new_password.setGeometry(QtCore.QRect(50, 120, 350, 31))
        self.new_password.setStyleSheet("border: none;\n"
                                        "border-bottom: 2px solid white;\n"
                                        "color: white;")
        self.new_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.new_password.setObjectName("new_password")

        # Trường xác nhận mật khẩu mới
        self.confirm_password = QtWidgets.QLineEdit(parent=self.groupBox_2)
        self.confirm_password.setGeometry(QtCore.QRect(50, 170, 350, 31))
        self.confirm_password.setStyleSheet("border: none;\n"
                                            "border-bottom: 2px solid white;\n"
                                            "color: white;")
        self.confirm_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.confirm_password.setObjectName("confirm_password")

        # Nút đặt lại mật khẩu
        self.reset_password_button = QtWidgets.QPushButton(parent=self.groupBox_2)
        self.reset_password_button.setGeometry(QtCore.QRect(50, 230, 350, 31))
        self.reset_password_button.setStyleSheet("border: 2px solid white;\n"
                                                 "color: white;\n"
                                                 "font: 12pt \"Times New Roman\";")
        self.reset_password_button.setObjectName("reset_password_button")

        # Nút quay lại đăng nhập
        self.back_to_login = QtWidgets.QPushButton(parent=self.groupBox_2)
        self.back_to_login.setGeometry(QtCore.QRect(50, 280, 350, 31))
        self.back_to_login.setStyleSheet("color: white;\n"
                                         "font: 10pt \"Times New Roman\";")
        self.back_to_login.setObjectName("back_to_login")

        self.horizontalLayout.addWidget(self.groupBox_2)
        spacerItem1 = QtWidgets.QSpacerItem(75, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)

        ForgotPasswordUI.setCentralWidget(self.centralwidget)

        self.retranslateUi(ForgotPasswordUI)
        QtCore.QMetaObject.connectSlotsByName(ForgotPasswordUI)

    def retranslateUi(self, ForgotPasswordUI):
        _translate = QtCore.QCoreApplication.translate
        ForgotPasswordUI.setWindowTitle(_translate("ForgotPasswordUI", "Quên mật khẩu"))
        self.label.setText(_translate("ForgotPasswordUI", "Quên mật khẩu"))
        self.email.setPlaceholderText(_translate("ForgotPasswordUI", "Nhập email của bạn"))
        self.new_password.setPlaceholderText(_translate("ForgotPasswordUI", "Nhập mật khẩu mới"))
        self.confirm_password.setPlaceholderText(_translate("ForgotPasswordUI", "Xác nhận mật khẩu mới"))
        self.reset_password_button.setText(_translate("ForgotPasswordUI", "Đặt lại mật khẩu"))
        self.back_to_login.setText(_translate("ForgotPasswordUI", "Quay lại đăng nhập"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ForgotPasswordUI = QtWidgets.QMainWindow()
    ui = Ui_ForgotPasswordUI()
    ui.setupUi(ForgotPasswordUI)
    ForgotPasswordUI.show()
    sys.exit(app.exec())
