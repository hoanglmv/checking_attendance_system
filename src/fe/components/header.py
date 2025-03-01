from PyQt6 import QtWidgets, QtCore

class Header(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMinimumSize(QtCore.QSize(0, 77))
        self.setMaximumSize(QtCore.QSize(16777215, 77))
        self.setStyleSheet("background-color: #192E44;")

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(20, 0, 20, 0)
        self.layout.setSpacing(10)
        
        # Title
        self.header_title = QtWidgets.QLabel("Điểm danh", self)
        self.header_title.setMinimumSize(QtCore.QSize(120, 37))
        self.header_title.setMaximumSize(QtCore.QSize(120, 37))
        self.header_title.setStyleSheet("color: white; font: 18pt 'Times New Roman';")
        self.layout.addWidget(self.header_title)
        
        self.layout.addStretch()
        
        # Company Info
        self.company_container = self.create_info_section(
            "src/fe/Image_and_icon/icons8-user-30.png", 
            "HKPTT Company", 240
        )
        self.layout.addWidget(self.company_container)
        
        # Year Info
        self.year_container = self.create_info_section(
            "src/fe/Image_and_icon/icons8-user-30.png", 
            "2025-2026", 160
        )
        self.layout.addWidget(self.year_container)
        
        # Spacer
        self.layout.addStretch()
        
        # Icons Section
        self.icon_container = self.create_icon_section()
        self.layout.addWidget(self.icon_container)
        
        # Admin Button
        self.btn_admin = QtWidgets.QPushButton(self)
        self.btn_admin.setMinimumSize(QtCore.QSize(35, 37))
        self.btn_admin.setMaximumSize(QtCore.QSize(35, 37))
        self.btn_admin.setStyleSheet(
            "background-color: #9FEF00; background-image: url(src/fe/Image_and_icon/icons8-user-30.png); "
            "background-repeat: no-repeat; background-position: center center; border-radius: 15px; border: 2px solid #a7a7a7;"
        )
        self.layout.addWidget(self.btn_admin)
    
    def create_info_section(self, icon_path, text, width):
        container = QtWidgets.QWidget(self)
        layout = QtWidgets.QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        
        icon_button = QtWidgets.QPushButton(self)
        icon_button.setMinimumSize(QtCore.QSize(30, 37))
        icon_button.setMaximumSize(QtCore.QSize(30, 37))
        icon_button.setStyleSheet(
            f"background-color: #9FEF00; background-image: url({icon_path}); background-repeat: no-repeat; background-position: center center;"
            "border-top-left-radius: 5px; border-bottom-left-radius: 5px;"
        )
        
        text_button = QtWidgets.QPushButton(text, self)
        text_button.setMinimumSize(QtCore.QSize(width, 37))
        text_button.setMaximumSize(QtCore.QSize(width, 37))
        text_button.setStyleSheet("border: 1px solid #9FEF00; border-top-right-radius: 5px; border-bottom-right-radius: 5px; color: white; font: 12pt 'Times New Roman';")
        
        layout.addWidget(icon_button)
        layout.addWidget(text_button)
        return container
    
    def create_icon_section(self):
        container = QtWidgets.QWidget(self)
        layout = QtWidgets.QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        
        icons = [
            "src/fe/Image_and_icon/icons8-plus-30.png",
            "src/fe/Image_and_icon/icons8-search-30.png",
            "src/fe/Image_and_icon/icons8-bell-40.png"
        ]
        
        for icon in icons:
            label = QtWidgets.QLabel(self)
            label.setMinimumSize(QtCore.QSize(40, 37))
            label.setMaximumSize(QtCore.QSize(40, 37))
            label.setStyleSheet(f"background-image: url({icon}); background-repeat: no-repeat; background-position: center center;")
            layout.addWidget(label)
        
        return container
