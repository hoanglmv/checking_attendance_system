from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class AdminInfoPopup(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup)
        self.setStyleSheet("""
            background-color: #122131;
            color: white;
            border: 2px solid #9FEF00;
            border-radius: 10px;
        """)
        self.resize(350, 400)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        avatar_label = QLabel(self)
        avatar_label.setFixedSize(50, 50)
        avatar_label.setStyleSheet("border-radius: 25px; background-color: #1B263B; padding: 5px;")
        pixmap = QPixmap("avatar.png") 
        avatar_label.setPixmap(pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(avatar_label, alignment=Qt.AlignmentFlag.AlignCenter)

        title = QLabel("ADMIN", self)
        title.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 5px; border: none;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Dữ liệu admin
        admin_info = {
            "ID": "20041",
            "Họ tên": "Lê Mai Việt H",
            "Chức vụ": "Nhân viên",
            "Nơi làm việc": "Phòng abc",
            "Email": "abc@gmail.com",
            "Số điện thoại": "0987 123 456"
        }

        for key, value in admin_info.items():
            row_layout = QHBoxLayout()
            label = QLabel(f"{key}:", self)
            label.setStyleSheet("font-size: 12px; min-width: 80px; border: none;")
            
            line_edit = QLineEdit(self)
            line_edit.setText(value)
            line_edit.setReadOnly(True)
            line_edit.setStyleSheet("""
                color: white;
                border: 1px solid white;
                padding: 5px;
                border-radius: 5px;
            """)

            row_layout.addWidget(label)
            row_layout.addWidget(line_edit)
            layout.addLayout(row_layout)

    def show_near(self, parent_widget):
        if parent_widget:
            parent_pos = parent_widget.mapToGlobal(parent_widget.rect().bottomRight())
            self.move(parent_pos.x() - self.width(), parent_pos.y())
        self.show()

    def focusOutEvent(self, event):
        self.close()
