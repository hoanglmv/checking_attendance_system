from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer

class NotificationPopup(QDialog):
    def __init__(self, message, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup)
        self.setStyleSheet("background-color: #0D1B2A; color: white; border-radius: 10px;")
        self.setFixedSize(300, 100)  # Kích thước cố định cho thông báo đơn lẻ

        # Layout chính
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        # Thông báo
        self.label = QLabel(message, self)
        self.label.setStyleSheet("""
            font-size: 14px; 
            color: #9FEF00; 
            background-color: rgba(159, 239, 0, 0.15); 
            padding: 5px; 
            border-radius: 5px;
        """)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        layout.addWidget(self.label)

        # Tự động đóng sau 5 giây
        QTimer.singleShot(5000, self.close)

    def show_near(self, parent_widget):
        """Hiển thị popup gần widget cha"""
        if parent_widget:
            parent_pos = parent_widget.mapToGlobal(parent_widget.rect().bottomRight())
            self.move(parent_pos.x() - self.width(), parent_pos.y())
        self.show()

    def focusOutEvent(self, event):
        """Đóng popup khi mất focus"""
        self.close()