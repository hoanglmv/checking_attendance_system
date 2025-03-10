from PyQt6 import QtWidgets, QtCore

class Header(QtWidgets.QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMinimumSize(QtCore.QSize(0, 77))
        self.setMaximumSize(QtCore.QSize(16777215, 77))
        self.setStyleSheet("background-color: #192E44;")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setContentsMargins(20, 0, 20, 0)
        self.horizontalLayout.setSpacing(0)
        
        # Title
        self.header_title = QtWidgets.QLabel("Điểm danh", self)
        self.header_title.setMinimumSize(QtCore.QSize(120, 37))
        self.header_title.setMaximumSize(QtCore.QSize(120, 37))
        self.header_title.setStyleSheet("color: white; font: 18pt 'Times New Roman';")
        self.horizontalLayout.addWidget(self.header_title)
        
        self.horizontalLayout.addStretch()
        
        # Company Info
        self.company_container = self.create_info_section(
            "src/fe/Image_and_icon/icons8-user-30.png", 
            "HKPTT Company", 240
        )
        self.horizontalLayout.addWidget(self.company_container)
        
        self.horizontalLayout.addSpacing(30)
        
        # Year Info
        self.year_container = self.create_info_section(
            "src/fe/Image_and_icon/icons8-user-30.png", 
            "2025-2026", 160
        )
        self.horizontalLayout.addWidget(self.year_container)
        
        self.horizontalLayout.addSpacing(10)
        
        # Icons Section
        self.icon_container = self.create_icon_section()
        self.horizontalLayout.addWidget(self.icon_container)
        
        self.horizontalLayout.addSpacing(20)
        
        # Admin Button
        self.btn_admin = QtWidgets.QPushButton(self)
        self.btn_admin.setMinimumSize(QtCore.QSize(35, 37))
        self.btn_admin.setMaximumSize(QtCore.QSize(35, 37))
        self.btn_admin.setStyleSheet(
            "background-color: #9FEF00; background-image: url(src/fe/Image_and_icon/icons8-user-30.png); "
            "background-repeat: no-repeat; background-position: center center; border-radius: 15px; border: 2px solid #a7a7a7;"
        )
        self.horizontalLayout.addWidget(self.btn_admin)
    
    def create_info_section(self, icon_path, text, width):
        container = QtWidgets.QWidget(self)
        layout = QtWidgets.QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
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

        icons = {
            "plus": "src/fe/Image_and_icon/icons8-plus-30.png",
            "search": "src/fe/Image_and_icon/icons8-search-30.png",
            "bell": "src/fe/Image_and_icon/icons8-bell-40.png"
        }

        self.buttons = {} 

        for key, icon in icons.items():
            btn = QtWidgets.QPushButton(self)
            btn.setMinimumSize(QtCore.QSize(40, 37))
            btn.setMaximumSize(QtCore.QSize(40, 37))
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    background-image: url({icon});
                    background-repeat: no-repeat;
                    background-position: center center;
                    border: none;
                }}
                QPushButton:hover {{
                    background-color: rgba(255, 255, 255, 0.1);
                }}
            """)

            self.buttons[key] = btn

            layout.addWidget(btn)

        return container

