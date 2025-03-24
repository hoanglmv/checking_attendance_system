from PyQt6 import QtWidgets, QtCore
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import QSettings
import requests
import subprocess
import os
import traceback
from pages.adminPopup import AdminInfoPopup  # Import AdminInfoPopup

def get_project_root():
    """
    Từ file Header nằm trong:
      (Đường dẫn tương tự)
    Đi lên 3 cấp sẽ cho ta thư mục gốc của dự án
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

class Header(QtWidgets.QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        print("Bắt đầu khởi tạo Header")  # Log để kiểm tra
        try:
            self.setMinimumSize(QtCore.QSize(0, 77))
            self.setMaximumSize(QtCore.QSize(16777215, 77))
            self.setStyleSheet("background-color: #192E44;")
            
            # Khởi tạo các biến tiến trình cho check-in và check-out
            self.process_checkin = None
            self.process_checkout = None

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
                "../Image_and_icon/icons8-user-30.png",  # Sửa đường dẫn
                "HKPTT Company", 240
            )
            self.horizontalLayout.addWidget(self.company_container)
            
            self.horizontalLayout.addSpacing(30)
            
            # Year Info
            self.year_container = self.create_info_section(
                "../Image_and_icon/icons8-user-30.png",  # Sửa đường dẫn
                "2025-2026", 160
            )
            self.horizontalLayout.addWidget(self.year_container)
            
            self.horizontalLayout.addSpacing(10)
            
            # Icons Section
            self.icon_container = self.create_icon_section()
            self.horizontalLayout.addWidget(self.icon_container)
            
            self.horizontalLayout.addSpacing(20)

            # Phần nút bật/tắt cam (Check-in & Check-out)
            self.camera_container = self.create_camera_section()
            self.horizontalLayout.addWidget(self.camera_container)

            self.horizontalLayout.addSpacing(20)
            
            # Admin Info Frame
            self.admin_frame = QtWidgets.QWidget(self)
            self.admin_frame_layout = QtWidgets.QHBoxLayout(self.admin_frame)
            self.admin_frame_layout.setContentsMargins(0, 0, 0, 0)
            self.admin_frame_layout.setSpacing(5)
            self.admin_frame.setStyleSheet("background-color: transparent;")
            self.admin_frame.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            self.admin_frame.mousePressEvent = self.show_admin_popup  # Gán sự kiện click

            # Tên admin
            self.admin_name = QtWidgets.QLabel("Admin", self.admin_frame)
            self.admin_name.setStyleSheet("color: white; font: 12pt 'Times New Roman'; font-weight: bold;")
            self.admin_frame_layout.addWidget(self.admin_name)
            self.horizontalLayout.addWidget(self.admin_frame)

            print("Hoàn tất khởi tạo giao diện Header")  # Log để kiểm tra

        except Exception as e:
            print(f"Lỗi khi khởi tạo Header: {str(e)}")
            traceback.print_exc()
    
    def create_camera_section(self):
        try:
            container = QtWidgets.QWidget(self)
            layout = QtWidgets.QHBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(10)
            
            # Nút Check-in
            self.btn_checkin = QtWidgets.QPushButton("Chạy Check-in", self)
            self.btn_checkin.setMinimumSize(QtCore.QSize(100, 37))
            self.btn_checkin.setStyleSheet("""
                QPushButton {
                    background-color: #2E86C1;
                    border: none;
                    border-radius: 5px;
                    color: white;
                    font: 12pt 'Times New Roman';
                    padding: 8px 16px;
                }
                QPushButton:hover {
                    background-color: #3498DB;
                }
                QPushButton:pressed {
                    background-color: #2980B9;
                }
            """)
            self.btn_checkin.clicked.connect(self.toggle_checkin)
            layout.addWidget(self.btn_checkin)
            
            # Nút Check-out
            self.btn_checkout = QtWidgets.QPushButton("Chạy Check-out", self)
            self.btn_checkout.setMinimumSize(QtCore.QSize(100, 37))
            self.btn_checkout.setStyleSheet("""
                QPushButton {
                    background-color: #2E86C1;
                    border: none;
                    border-radius: 5px;
                    color: white;
                    font: 12pt 'Times New Roman';
                    padding: 8px 16px;
                }
                QPushButton:hover {
                    background-color: #3498DB;
                }
                QPushButton:pressed {
                    background-color: #2980B9;
                }
            """)
            self.btn_checkout.clicked.connect(self.toggle_checkout)
            layout.addWidget(self.btn_checkout)
            
            return container
        except Exception as e:
            print(f"Lỗi khi tạo camera section: {str(e)}")
            traceback.print_exc()
            return QtWidgets.QWidget(self)

    def toggle_checkin(self):
        """Bật/Tắt chạy file checkin.py"""
        if self.process_checkin is None:
            try:
                working_dir = get_project_root()  # Thư mục gốc của dự án
                # Xây dựng đường dẫn đến checkin.py tương đối với thư mục gốc
                checkin_path = os.path.join("src", "be-src", "app", "tool", "checkin.py")
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
        """Bật/Tắt chạy file checkout.py"""
        if self.process_checkout is None:
            try:
                working_dir = get_project_root()  # Thư mục gốc của dự án
                checkout_path = os.path.join("src", "be-src", "app", "tool", "checkout.py")
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
        """Tải thông tin admin từ API để hiển thị tên"""
        print("Bắt đầu load_admin_info")  # Log để kiểm tra
        try:
            settings = QSettings("MyApp", "LoginApp")
            access_token = settings.value("access_token")
            if not access_token:
                print("Không tìm thấy access_token để tải thông tin admin! Kiểm tra xem access_token đã được lưu trong QSettings chưa.")
                self.admin_name.setText("Admin")
                self.admin_name.update()  # Cập nhật giao diện
                print(f"Đã đặt tên admin là: {self.admin_name.text()} (do không có access_token)")
                return

            print(f"Access token: {access_token}")

            api_url = "http://127.0.0.1:8000/auth/me"
            headers = {"Authorization": f"Bearer {access_token}"}
            print("Gửi yêu cầu đến API /auth/me")
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()

            admin_info = response.json()
            print(f"Thông tin admin trong Header: {admin_info}")

            # Kiểm tra dữ liệu trả về
            if not isinstance(admin_info, dict):
                print(f"Dữ liệu trả về từ API không phải là dictionary! Dữ liệu nhận được: {admin_info}")
                self.admin_name.setText("Admin")
                self.admin_name.update()  # Cập nhật giao diện
                print(f"Đã đặt tên admin là: {self.admin_name.text()} (do dữ liệu không phải dictionary)")
                return

            # Cập nhật tên
            full_name = admin_info.get("full_name", "Admin")
            print(f"Giá trị full_name từ API: '{full_name}'")
            if not full_name or not full_name.strip():
                print("full_name rỗng hoặc chỉ chứa khoảng trắng, đặt giá trị mặc định là 'Admin'")
                full_name = "Admin"
            self.admin_name.setText(full_name)
            self.admin_name.update()  # Cập nhật giao diện
            print(f"Đã đặt tên admin là: {self.admin_name.text()}")

        except requests.RequestException as e:
            print(f"Lỗi khi gọi API /auth/me trong Header: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Chi tiết lỗi: {e.response.status_code} - {e.response.text}")
            else:
                print("Không nhận được phản hồi từ server. Kiểm tra xem backend có đang chạy không.")
            self.admin_name.setText("Admin")
            self.admin_name.update()  # Cập nhật giao diện
            print(f"Đã đặt tên admin là: {self.admin_name.text()} (do lỗi API)")
        except Exception as e:
            print(f"Lỗi không xác định khi tải thông tin admin trong Header: {str(e)}")
            traceback.print_exc()
            self.admin_name.setText("Admin")
            self.admin_name.update()  # Cập nhật giao diện
            print(f"Đã đặt tên admin là: {self.admin_name.text()} (do lỗi không xác định)")

    def refresh_admin_info(self):
        """Phương thức công khai để gọi lại load_admin_info"""
        print("Gọi refresh_admin_info")
        self.load_admin_info()

    def show_admin_popup(self, event):
        """Hiển thị popup thông tin admin khi bấm vào khung"""
        try:
            print(f"Tên admin hiện tại trước khi mở popup: {self.admin_name.text()}")  # Log để kiểm tra
            popup = AdminInfoPopup(self)
            popup.show_near(self.admin_frame)
        except Exception as e:
            print(f"Lỗi khi hiển thị AdminInfoPopup: {str(e)}")
            traceback.print_exc()

    def create_info_section(self, icon_path, text, width):
        try:
            # Kiểm tra xem icon_path có tồn tại không
            if not os.path.exists(icon_path):
                print(f"Không tìm thấy file icon tại: {icon_path}")
                icon_path = ""  # Nếu không tìm thấy, không hiển thị icon

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
        except Exception as e:
            print(f"Lỗi khi tạo info section: {str(e)}")
            traceback.print_exc()
            return QtWidgets.QWidget(self)

    def create_icon_section(self):
        try:
            container = QtWidgets.QWidget(self)
            layout = QtWidgets.QHBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)

            icons = {
                "plus": "../Image_and_icon/icons8-plus-30.png",  # Sửa đường dẫn
                "search": "../Image_and_icon/icons8-search-30.png",  # Sửa đường dẫn
                "bell": "../Image_and_icon/icons8-bell-40.png"  # Sửa đường dẫn
            }

            self.buttons = {}

            for key, icon in icons.items():
                # Kiểm tra xem icon có tồn tại không
                if not os.path.exists(icon):
                    print(f"Không tìm thấy file icon tại: {icon}")
                    icon = ""  # Nếu không tìm thấy, không hiển thị icon

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
        except Exception as e:
            print(f"Lỗi khi tạo icon section: {str(e)}")
            traceback.print_exc()
            return QtWidgets.QWidget(self)
