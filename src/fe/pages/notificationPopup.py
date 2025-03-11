from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt


class NotificationPopup(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup) 
        self.setStyleSheet("background-color: #0D1B2A; color: white; border-radius: 10px;")
        self.resize(400, 600)

        layout = QVBoxLayout(self)

        title = QLabel("Thông báo", self)
        title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 5px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.listWidget = QListWidget(self)
        self.listWidget.setStyleSheet("background-color: #1B263B; color: white; font-size: 14px; padding: 5px; border: 1px solid #9FEF00")

        notifications = [
            "Lê Doãn T checkin lúc 9:00 AM",
            "ABC checkin lúc 8:30 AM",
            "Lê Doãn T checkin lúc 8:00 AM",
            "Lê Doãn T checkin lúc 7:50 AM",
        ]

        for text in notifications:
            item = QListWidgetItem(text)
            self.listWidget.addItem(item)

        layout.addWidget(self.listWidget)

    def show_near(self, parent_widget):
        if parent_widget:
            parent_pos = parent_widget.mapToGlobal(parent_widget.rect().bottomRight())
            self.move(parent_pos.x() - self.width(), parent_pos.y())
        self.show()

    def focusOutEvent(self, event):
        self.close()
