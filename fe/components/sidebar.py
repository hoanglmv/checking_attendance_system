from PyQt6 import QtWidgets, QtCore

class Sidebar(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMinimumSize(QtCore.QSize(280, 0))
        self.setMaximumSize(QtCore.QSize(280, 16777215))
        self.setStyleSheet("background-color: #122131;")

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(35, 0, 35, 0)
        self.verticalLayout.setSpacing(10)

        # Logo
        self.logo = QtWidgets.QLabel(self)
        self.logo.setMinimumSize(QtCore.QSize(200, 180))
        self.logo.setMaximumSize(QtCore.QSize(200, 180))
        self.logo.setStyleSheet("""
            background-image: url(D:/NMCNPM/checking_attendance_system/fe/Image_and_icon/logo.png);
            background-repeat: no-repeat;
            background-position: center center;
            background-size: contain;
        """)
        self.verticalLayout.addWidget(self.logo)

        # Button: Attendance
        self.fil_attendance = self.create_button_container()
        self.btn_attendance = self.create_button(
            "D:/NMCNPM/checking_attendance_system/fe/Image_and_icon/icons8-user-30.png",
            "Điểm danh"
        )
        self.fil_attendance.layout().addWidget(self.btn_attendance)
        self.verticalLayout.addWidget(self.fil_attendance)

        # Button: Manage
        self.fil_manage = self.create_button_container()
        self.btn_manage = self.create_button(
            "D:/NMCNPM/checking_attendance_system/fe/Image_and_icon/icons8-user-30.png",
            "Quản lý"
        )
        self.fil_manage.layout().addWidget(self.btn_manage)
        self.verticalLayout.addWidget(self.fil_manage)

        # Spacer
        spacer = QtWidgets.QSpacerItem(20, 300, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacer)

        # Button: Logout
        self.fil_logout = self.create_button_container()
        self.btn_logout = self.create_button(
            "D:/NMCNPM/checking_attendance_system/fe/Image_and_icon/icons8-user-30.png",
            "Đăng xuất"
        )
        self.fil_logout.layout().addWidget(self.btn_logout)
        self.verticalLayout.addWidget(self.fil_logout)

    def create_button_container(self):
        container = QtWidgets.QGroupBox(self)
        container.setMinimumSize(QtCore.QSize(200, 58))
        container.setMaximumSize(QtCore.QSize(200, 58))
        container.setStyleSheet("background-color: #122131; border-radius: 5px;")
        layout = QtWidgets.QGridLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        return container

    def create_button(self, icon_path, text):
        button = QtWidgets.QPushButton(self)
        button.setMinimumSize(QtCore.QSize(180, 32))
        button.setMaximumSize(QtCore.QSize(180, 32))
        button.setText(text)
        button.setStyleSheet(f"""
            background-image: url({icon_path});
            background-repeat: no-repeat;
            background-position: center center;
            background-size: 24px 24px;
            color: white;
            font: 12pt "Times New Roman";
            padding-left: 40px;
        """)
        return button
