from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QPushButton, QMessageBox
from PyQt6.QtCore import Qt, QSettings
import requests
import traceback

class AdminInfoPopup(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        try:
            self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup)
            self.setStyleSheet("""
                background-color: #122131;
                color: white;
                border: 2px solid #9FEF00;
                border-radius: 10px;
            """)
            self.resize(350, 350)

            self.layout = QVBoxLayout(self)
            self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Tên admin
            self.title = QLabel("ADMIN", self)
            self.title.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 5px; border: none;")
            self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.layout.addWidget(self.title)

            # Dữ liệu admin (sẽ được lấy từ API)
            self.admin_info = {}
            self.line_edits = {}
            self.is_editing = False  # Trạng thái chỉnh sửa

            # Hiển thị thông tin admin
            info_fields = {
                "Họ tên": "full_name",
                "Chức vụ": "position",
                "Nơi làm việc": "department",
                "Email": "email",
                "Số điện thoại": "phone"
            }

            for label_text, field in info_fields.items():
                row_layout = QHBoxLayout()
                label = QLabel(f"{label_text}:", self)
                label.setStyleSheet("font-size: 12px; min-width: 80px; border: none;")

                line_edit = QLineEdit(self)
                line_edit.setText("")
                line_edit.setReadOnly(True)
                line_edit.setStyleSheet("""
                    color: white;
                    border: 1px solid white;
                    padding: 5px;
                    border-radius: 5px;
                """)

                self.line_edits[label_text] = line_edit
                row_layout.addWidget(label)
                row_layout.addWidget(line_edit)
                self.layout.addLayout(row_layout)

            # Nút cập nhật/lưu
            self.update_button = QPushButton("Cập nhật hồ sơ", self)
            self.update_button.setStyleSheet("""
                QPushButton {
                    background-color: #68D477;
                    color: black;
                    padding: 8px 16px;
                    border-radius: 5px;
                    font-size: 12px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #5AC469;
                }
            """)
            self.update_button.clicked.connect(self.toggle_edit_mode)
            self.layout.addWidget(self.update_button, alignment=Qt.AlignmentFlag.AlignCenter)

            # Tải thông tin admin
            self.load_admin_info()

        except Exception as e:
            print(f"Lỗi khi khởi tạo AdminInfoPopup: {str(e)}")
            traceback.print_exc()
            QMessageBox.critical(self, "Lỗi", f"Không thể khởi tạo popup: {str(e)}")
            self.close()

    def load_admin_info(self):
        """Gọi API để lấy thông tin admin"""
        try:
            settings = QSettings("MyApp", "LoginApp")
            access_token = settings.value("access_token")
            if not access_token:
                print("Không tìm thấy access_token để tải thông tin admin!")
                QMessageBox.critical(self, "Lỗi", "Không tìm thấy access_token. Vui lòng đăng nhập lại!")
                self.close()
                return

            api_url = "http://127.0.0.1:8000/auth/me"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()

            self.admin_info = response.json()
            print(f"Thông tin admin: {self.admin_info}")

            # Kiểm tra dữ liệu trả về
            if not isinstance(self.admin_info, dict):
                raise ValueError("Dữ liệu trả về từ API không phải là dictionary!")

            # Cập nhật tiêu đề (tên admin)
            self.title.setText(self.admin_info.get("full_name", "ADMIN"))

            # Cập nhật các trường thông tin
            for label_text, field in zip(
                ["Họ tên", "Chức vụ", "Nơi làm việc", "Email", "Số điện thoại"],
                ["full_name", "position", "department", "email", "phone"]
            ):
                value = str(self.admin_info.get(field, ""))
                self.line_edits[label_text].setText(value)

        except requests.RequestException as e:
            print(f"Lỗi khi gọi API /auth/me: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Chi tiết lỗi: {e.response.status_code} - {e.response.text}")
            QMessageBox.critical(self, "Lỗi", f"Không thể tải thông tin admin: {str(e)}")
            self.close()
        except Exception as e:
            print(f"Lỗi không xác định khi tải thông tin admin: {str(e)}")
            traceback.print_exc()
            QMessageBox.critical(self, "Lỗi", f"Lỗi không xác định: {str(e)}")
            self.close()

    def toggle_edit_mode(self):
        """Chuyển đổi giữa chế độ xem và chế độ chỉnh sửa"""
        try:
            self.is_editing = not self.is_editing

            for label_text, line_edit in self.line_edits.items():
                if label_text == "Email":
                    line_edit.setReadOnly(True)  # Email luôn chỉ đọc
                    line_edit.setStyleSheet("""
                        color: gray;
                        border: 1px solid white;
                        padding: 5px;
                        border-radius: 5px;
                    """)
                else:
                    line_edit.setReadOnly(not self.is_editing)
                    if self.is_editing:
                        line_edit.setStyleSheet("""
                            color: white;
                            border: 1px solid #68D477;
                            padding: 5px;
                            border-radius: 5px;
                            background-color: #1B263B;
                        """)
                    else:
                        line_edit.setStyleSheet("""
                            color: white;
                            border: 1px solid white;
                            padding: 5px;
                            border-radius: 5px;
                        """)

            if self.is_editing:
                self.update_button.setText("Lưu thay đổi")
                self.update_button.setStyleSheet("""
                    QPushButton {
                        background-color: #FFA500;
                        color: black;
                        padding: 8px 16px;
                        border-radius: 5px;
                        font-size: 12px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #E69500;
                    }
                """)
            else:
                self.save_changes()
                self.update_button.setText("Cập nhật hồ sơ")
                self.update_button.setStyleSheet("""
                    QPushButton {
                        background-color: #68D477;
                        color: black;
                        padding: 8px 16px;
                        border-radius: 5px;
                        font-size: 12px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #5AC469;
                    }
                """)

        except Exception as e:
            print(f"Lỗi khi chuyển đổi chế độ chỉnh sửa: {str(e)}")
            traceback.print_exc()
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi chuyển đổi chế độ: {str(e)}")

    def save_changes(self):
        """Lưu thay đổi thông tin admin qua API"""
        try:
            settings = QSettings("MyApp", "LoginApp")
            access_token = settings.value("access_token")
            if not access_token:
                print("Không tìm thấy access_token để lưu thông tin admin!")
                QMessageBox.critical(self, "Lỗi", "Không tìm thấy access_token. Vui lòng đăng nhập lại!")
                self.is_editing = True  # Giữ chế độ chỉnh sửa nếu có lỗi
                return

            update_data = {
                "full_name": self.line_edits["Họ tên"].text(),
                "position": self.line_edits["Chức vụ"].text(),
                "department": self.line_edits["Nơi làm việc"].text(),
                "phone": self.line_edits["Số điện thoại"].text(),
            }

            # Kiểm tra trường full_name không được rỗng
            if not update_data["full_name"].strip():
                QMessageBox.warning(self, "Lỗi", "Họ tên không được để trống!")
                self.is_editing = True  # Giữ chế độ chỉnh sửa nếu có lỗi
                return

            api_url = "http://127.0.0.1:8000/auth/me/update"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.put(api_url, data=update_data, headers=headers)
            response.raise_for_status()

            # Cập nhật lại thông tin admin sau khi lưu
            self.admin_info.update(update_data)
            self.title.setText(self.admin_info.get("full_name", "ADMIN"))
            QMessageBox.information(self, "Thành công", "Cập nhật thông tin thành công!")

            # Cập nhật tên trong Header nếu có
            if hasattr(self.parent(), 'load_admin_info'):
                self.parent().load_admin_info()

        except requests.RequestException as e:
            print(f"Lỗi khi gọi API /auth/me/update: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Chi tiết lỗi: {e.response.status_code} - {e.response.text}")
            QMessageBox.critical(self, "Lỗi", f"Cập nhật thất bại: {str(e)}")
            self.is_editing = True  # Giữ chế độ chỉnh sửa nếu có lỗi
        except Exception as e:
            print(f"Lỗi không xác định khi lưu thông tin admin: {str(e)}")
            traceback.print_exc()
            QMessageBox.critical(self, "Lỗi", f"Lỗi không xác định: {str(e)}")
            self.is_editing = True  # Giữ chế độ chỉnh sửa nếu có lỗi

    def show_near(self, parent_widget):
        try:
            if parent_widget:
                parent_pos = parent_widget.mapToGlobal(parent_widget.rect().bottomRight())
                self.move(parent_pos.x() - self.width(), parent_pos.y())
            self.show()
        except Exception as e:
            print(f"Lỗi khi hiển thị popup: {str(e)}")
            traceback.print_exc()
            QMessageBox.critical(self, "Lỗi", f"Không thể hiển thị popup: {str(e)}")
            self.close()

    def focusOutEvent(self, event):
        try:
            self.close()
        except Exception as e:
            print(f"Lỗi khi đóng popup: {str(e)}")
            traceback.print_exc()