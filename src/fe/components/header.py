# header.py
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import QSettings, QTimer
import requests
import subprocess
import os
import traceback
import json
from pages.adminPopup import AdminInfoPopup
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

def get_project_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

class NotificationPopup(QDialog):
    def __init__(self, message, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup)
        self.setStyleSheet("background-color: #0D1B2A; color: white; border-radius: 10px;")
        self.setFixedSize(300, 100)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

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

        QTimer.singleShot(5000, self.close)

    def show_near(self, parent_widget):
        if parent_widget:
            parent_pos = parent_widget.mapToGlobal(parent_widget.rect().bottomRight())
            self.move(parent_pos.x() - self.width(), parent_pos.y())
        self.show()

    def focusOutEvent(self, event):
        self.close()

class Header(QtWidgets.QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        print("Bắt đầu khởi tạo Header")
        try:
            self.setMinimumSize(QtCore.QSize(0, 77))
            self.setMaximumSize(QtCore.QSize(16777215, 77))
            self.setStyleSheet("background-color: #192E44;")
            
            self.process_checkin = None
            self.process_checkout = None
            self.notification_popup = None

            self.horizontalLayout = QtWidgets.QHBoxLayout(self)
            self.horizontalLayout.setContentsMargins(15, 0, 15, 0)
            self.horizontalLayout.setSpacing(15)
            
            self.header_title = QtWidgets.QLabel("Điểm danh", self)
            self.header_title.setFixedSize(QtCore.QSize(120, 37))
            self.header_title.setStyleSheet("color: white; font: 18pt 'Times New Roman';")
            self.header_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.horizontalLayout.addWidget(self.header_title)
            
            self.horizontalLayout.addStretch(1)
            
            self.company_container = self.create_info_section("HKPTT Company", 200)
            self.horizontalLayout.addWidget(self.company_container)
            
            self.horizontalLayout.addSpacing(20)
            
            self.year_container = self.create_info_section("2025-2026", 140)
            self.horizontalLayout.addWidget(self.year_container)
            
            self.horizontalLayout.addSpacing(20)

            self.camera_container = self.create_camera_section()
            self.horizontalLayout.addWidget(self.camera_container)

            self.horizontalLayout.addSpacing(20)
            
            self.checkin_notification = QtWidgets.QLabel("", self)
            self.checkin_notification.setStyleSheet("""
                color: #9FEF00; 
                font: 11pt 'Times New Roman'; 
                background-color: rgba(159, 239, 0, 0.15); 
                border-radius: 5px; 
                padding: 5px;
            """)
            self.checkin_notification.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.checkin_notification.setMaximumWidth(350)
            self.checkin_notification.setWordWrap(True)
            self.horizontalLayout.addWidget(self.checkin_notification)

            self.horizontalLayout.addSpacing(20)
            
            self.admin_frame = QtWidgets.QWidget(self)
            self.admin_frame_layout = QtWidgets.QHBoxLayout(self.admin_frame)
            self.admin_frame_layout.setContentsMargins(0, 0, 0, 0)
            self.admin_frame_layout.setSpacing(5)
            self.admin_frame.setStyleSheet("background-color: transparent;")
            self.admin_frame.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            self.admin_frame.mousePressEvent = self.show_admin_popup

            self.admin_name = QtWidgets.QLabel("Chưa đăng nhập", self.admin_frame)
            self.admin_name.setStyleSheet("color: white; font: 12pt 'Times New Roman'; font-weight: bold;")
            self.admin_name.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            self.admin_frame_layout.addWidget(self.admin_name)
            self.horizontalLayout.addWidget(self.admin_frame)

            self.horizontalLayout.addStretch(1)

            self.checkin_timer = QTimer(self)
            self.checkin_timer.timeout.connect(self.check_checkin_notification)
            self.checkin_timer.start(1000)

            print("Hoàn tất khởi tạo giao diện Header")

        except Exception as e:
            print(f"Lỗi khi khởi tạo Header: {str(e)}")
            traceback.print_exc()

    def check_checkin_notification(self):
        temp_file = os.path.join(get_project_root(), "checkin_notification.json")
        if os.path.exists(temp_file):
            try:
                with open(temp_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                employee_full_name = data.get("full_name", "Unknown")
                check_in_time = data.get("check_in_time", "N/A")
                status = data.get("status", "success")
                
                if status == "already_checked_in":
                    message = f"Nhân viên {employee_full_name} đã điểm danh hôm nay rồi"
                else:
                    message = f"Đã check-in thành công cho {employee_full_name} lúc {check_in_time}"
                
                self.checkin_notification.setText(message)
                
                if self.notification_popup:
                    self.notification_popup.close()
                self.notification_popup = NotificationPopup(message, self)
                self.notification_popup.show_near(self)
                
                print(f"Đã cập nhật thông báo: {message}")
                os.remove(temp_file)
                QTimer.singleShot(5000, lambda: self.checkin_notification.setText(""))
            except Exception as e:
                print(f"Lỗi khi đọc file thông báo check-in: {str(e)}")

    def create_camera_section(self):
        try:
            container = QtWidgets.QWidget(self)
            layout = QtWidgets.QHBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(15)
            
            self.btn_checkin = QtWidgets.QPushButton("Chạy Check-in", self)
            self.btn_checkin.setFixedSize(QtCore.QSize(130, 40))
            self.btn_checkin.setStyleSheet("""
                QPushButton { background-color: #2E86C1; border: none; border-radius: 5px; color: white; font: 11pt 'Times New Roman'; }
                QPushButton:hover { background-color: #3498DB; border: 1px solid #FFFFFF; }
                QPushButton:pressed { background-color: #2980B9; }
            """)
            self.btn_checkin.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            self.btn_checkin.clicked.connect(self.toggle_checkin)
            layout.addWidget(self.btn_checkin)
            
            self.btn_checkout = QtWidgets.QPushButton("Chạy Check-out", self)
            self.btn_checkout.setFixedSize(QtCore.QSize(130, 40))
            self.btn_checkout.setStyleSheet("""
                QPushButton { background-color: #2E86C1; border: none; border-radius: 5px; color: white; font: 11pt 'Times New Roman'; }
                QPushButton:hover { background-color: #3498DB; border: 1px solid #FFFFFF; }
                QPushButton:pressed { background-color: #2980B9; }
            """)
            self.btn_checkout.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            self.btn_checkout.clicked.connect(self.toggle_checkout)
            layout.addWidget(self.btn_checkout)
            
            return container
        except Exception as e:
            print(f"Lỗi khi tạo camera section: {str(e)}")
            traceback.print_exc()
            return QtWidgets.QWidget(self)

    def toggle_checkin(self):
        if self.process_checkin is None:
            try:
                working_dir = get_project_root()
                checkin_path = os.path.join("src", "be_src", "app", "tool", "checkin.py")
                self.process_checkin = subprocess.Popen(["python", checkin_path], cwd=working_dir)
                self.btn_checkin.setText("Dừng Check-in")
                print("Đã mở checkin.py")
            except Exception as e:
                print(f"Lỗi khi mở checkin.py: {e}")
        else:
            self.process_checkin.terminate()
            self.process_checkin = None
            self.btn_checkin.setText("Chạy Check-in")
            print("Đã đóng checkin.py")

    def toggle_checkout(self):
        if self.process_checkout is None:
            try:
                working_dir = get_project_root()
                checkout_path = os.path.join("src", "be_src", "app", "tool", "checkout.py")
                self.process_checkout = subprocess.Popen(["python", checkout_path], cwd=working_dir)
                self.btn_checkout.setText("Dừng Check-out")
                print("Đã mở checkout.py")
            except Exception as e:
                print(f"Lỗi khi mở checkout.py: {e}")
        else:
            self.process_checkout.terminate()
            self.process_checkout = None
            self.btn_checkout.setText("Chạy Check-out")
            print("Đã đóng checkout.py")

    def load_admin_info(self):
        print("Bắt đầu load_admin_info")
        try:
            settings = QSettings("MyApp", "LoginApp")
            access_token = settings.value("access_token", None)
            print(f"Token trong load_admin_info: {access_token}")
            if not access_token:
                print("Không tìm thấy access_token, không gọi API /auth/me")
                self.admin_name.setText("Chưa đăng nhập")
                self.admin_name.update()
                return
            api_url = "http://127.0.0.1:8000/auth/me"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(api_url, headers=headers)
            if response.status_code == 200:
                try:
                    admin_info = response.json()
                    full_name = admin_info.get("full_name", "Admin")
                    if not full_name or not full_name.strip():
                        full_name = "Admin"
                    self.admin_name.setText(full_name)
                    self.admin_name.update()
                    print(f"Đã đặt tên admin là: {self.admin_name.text()}")
                except ValueError as e:
                    print(f"Lỗi khi parse JSON từ /auth/me: {str(e)}")
                    self.admin_name.setText("Chưa đăng nhập")
                    self.admin_name.update()
            else:
                print(f"API /auth/me trả về lỗi: {response.status_code} - {response.text}")
                self.admin_name.setText("Chưa đăng nhập")
                self.admin_name.update()
        except requests.RequestException as e:
            print(f"Lỗi khi gọi API /auth/me: {str(e)}")
            self.admin_name.setText("Chưa đăng nhập")
            self.admin_name.update()
        except Exception as e:
            print(f"Lỗi không xác định khi tải thông tin admin: {str(e)}")
            traceback.print_exc()
            self.admin_name.setText("Chưa đăng nhập")
            self.admin_name.update()

    def refresh_admin_info(self):
        print("Gọi refresh_admin_info")
        self.load_admin_info()

    def show_admin_popup(self, event):
        try:
            print(f"Tên admin hiện tại trước khi mở popup: {self.admin_name.text()}")
            popup = AdminInfoPopup(self)
            popup.show_near(self.admin_frame)
        except Exception as e:
            print(f"Lỗi khi hiển thị AdminInfoPopup: {str(e)}")
            traceback.print_exc()

    def create_info_section(self, text, width):
        try:
            container = QtWidgets.QWidget(self)
            layout = QtWidgets.QHBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)
            text_button = QtWidgets.QPushButton(text, self)
            text_button.setFixedSize(QtCore.QSize(width, 37))
            self.header_title.setText("Điểm danh")
            text_button.setStyleSheet("""
                QPushButton { background-color: #34495E; border: 1px solid #9FEF00; border-radius: 5px; color: white; font: 11pt 'Times New Roman'; }
                QPushButton:hover { background-color: #3D5A80; border: 1px solid #FFFFFF; }
            """)
            text_button.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            layout.addWidget(text_button)
            return container
        except Exception as e:
            print(f"Lỗi khi tạo info section: {str(e)}")
            traceback.print_exc()
            return QtWidgets.QWidget(self)

    def create_icon_section(self):
        try:
            container = QtWidgets.QWidget(self)
            layout = QtWidgets.QHBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)
            return container
        except Exception as e:
            print(f"Lỗi khi tạo icon section: {str(e)}")
            traceback.print_exc()
            return QtWidgets.QWidget(self)