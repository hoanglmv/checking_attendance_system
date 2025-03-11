import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel

app = QApplication(sys.argv)
window = QMainWindow()
tab_widget = QTabWidget()

tab1 = QWidget()
tab1_layout = QVBoxLayout(tab1)
tab1_layout.addWidget(QLabel("Tab 1"))

tab2 = QWidget()
tab2_layout = QVBoxLayout(tab2)
tab2_layout.addWidget(QLabel("Tab 2"))

tab_widget.addTab(tab1, "Tab 1")
tab_widget.addTab(tab2, "Tab 2")

window.setCentralWidget(tab_widget)
window.show()
sys.exit(app.exec())


        # self.tab2Layout.setSpacing(20)
        # self.tab2Layout.setContentsMargins(20, 20, 20, 20)

        # # Tiêu đề
        # self.addEmployeeLabel = QLabel("Thêm Nhân Viên Mới")
        # self.addEmployeeLabel.setStyleSheet("""
        #     color: white;
        #     font-size: 24px;
        #     font-weight: bold;
        #     margin-bottom: 20px;
        # """)
        # self.tab2Layout.addWidget(self.addEmployeeLabel)

        # # Form nhập thông tin
        # self.formLayout = QGridLayout()
        # self.formLayout.setSpacing(15)

        # # Các trường nhập liệu
        # self.fields = {
        #     "Họ tên:": QLineEdit(),
        #     "ID:": QLineEdit(),
        #     "Chức vụ:": QLineEdit(),
        #     "Nơi làm việc:": QLineEdit(),
        #     "Email:": QLineEdit(),
        #     "Số điện thoại:": QLineEdit()
        # }

        # # Thêm các trường vào form
        # row = 0
        # for label_text, line_edit in self.fields.items():
        #     label = QLabel(label_text)
        #     label.setStyleSheet("color: white; font-size: 16px;")
        #     line_edit.setStyleSheet("""
        #         background-color: white;
        #         color: black;
        #         font-size: 14px;
        #         padding: 8px;
        #         border-radius: 5px;
        #     """)
        #     self.formLayout.addWidget(label, row, 0)
        #     self.formLayout.addWidget(line_edit, row, 1)
        #     row += 1

        # # Thêm form vào layout của tab 2
        # self.tab2Layout.addLayout(self.formLayout)

        # # Nút "Thêm ảnh"
        # self.uploadPhotoButton = QPushButton("Thêm Ảnh Đại Diện")
        # self.uploadPhotoButton.setStyleSheet("""
        #     QPushButton {
        #         background-color: #68D477;
        #         color: black;
        #         padding: 10px;
        #         border-radius: 5px;
        #         font-size: 14px;
        #     }
        #     QPushButton:hover {
        #         background-color: #5AC469;
        #     }
        # """)
        # self.tab2Layout.addWidget(self.uploadPhotoButton, alignment=Qt.AlignmentFlag.AlignCenter)

        # # Nút "Thêm nhân viên"
        # self.addButton = QPushButton("Thêm Nhân Viên")
        # self.addButton.setStyleSheet("""
        #     QPushButton {
        #         background-color: #4CAF50;
        #         color: white;
        #         padding: 12px 24px;
        #         border-radius: 5px;
        #         font-size: 16px;
        #         font-weight: bold;
        #     }
        #     QPushButton:hover {
        #         background-color: #45a049;
        #     }
        # """)
        # self.tab2Layout.addWidget(self.addButton, alignment=Qt.AlignmentFlag.AlignCenter)

        # # Kết nối sự kiện cho nút "Thêm nhân viên"
        # self.addButton.clicked.connect(self.addEmployee)

        # # Kết nối sự kiện cho nút "Thêm ảnh"
        # self.uploadPhotoButton.clicked.connect(self.uploadPhoto)

        

        # # Biến lưu đường dẫn ảnh
        # self.photoPath = None

        # def uploadPhoto(self):
        #     # Mở hộp thoại chọn ảnh
        #     file_dialog = QtWidgets.QFileDialog()
        #     file_path, _ = file_dialog.getOpenFileName(None, "Chọn ảnh đại diện", "", "Images (*.png *.jpg *.jpeg)")
        #     if file_path:
        #         self.photoPath = file_path
        #         QtWidgets.QMessageBox.information(None, "Thành công", "Ảnh đã được chọn!")

        # def addEmployee(self):
        #     # Lấy dữ liệu từ các trường nhập liệu
        #     name = self.fields["Họ tên:"].text()
        #     emp_id = self.fields["ID:"].text()
        #     position = self.fields["Chức vụ:"].text()
        #     office = self.fields["Nơi làm việc:"].text()
        #     email = self.fields["Email:"].text()
        #     phone = self.fields["Số điện thoại:"].text()

        #     # Kiểm tra các trường bắt buộc
        #     if not name or not emp_id or not position or not office:
        #         QtWidgets.QMessageBox.warning(None, "Lỗi", "Vui lòng điền đầy đủ thông tin bắt buộc!")
        #         return

        #     # Thêm nhân viên vào danh sách
        #     new_employee = {
        #         "id": emp_id,
        #         "name": name,
        #         "position": position,
        #         "office": office,
        #         "email": email,
        #         "phone": phone,
        #         "photo": self.photoPath
        #     }

        #     # Thêm vào danh sách nhân viên
        #     self.employees.append(new_employee)

        #     # Cập nhật danh sách trong tab 1
        #     self.updateEmployeeList()

        #     # Thông báo thành công
        #     QtWidgets.QMessageBox.information(None, "Thành công", "Nhân viên đã được thêm thành công!")

        #     # Xóa các trường nhập liệu
        #     for field in self.fields.values():
        #         field.clear()
        #     self.photoPath = None

        # def updateEmployeeList(self):
        #     # Xóa danh sách hiện tại
        #     self.employeeList.clear()

        #     # Thêm lại tất cả nhân viên vào danh sách
        #     for emp in self.employees:
        #         item = QListWidgetItem()
        #         itemWidget = QWidget()
        #         layout = QHBoxLayout(itemWidget)
        #         layout.setContentsMargins(10, 10, 10, 10)
        #         layout.setSpacing(50)
        #         layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        #         photoLabel = QLabel()
        #         photoLabel.setFixedSize(80, 80)
        #         photoLabel.setStyleSheet("border-radius: 30px; border: 2px solid white;")

        #         info = QLabel(f"ID: {emp['id']}\nHọ tên: {emp['name']}\nChức vụ: {emp['position']}\nNơi làm việc: {emp['office']}")
        #         info.setStyleSheet("color: white; font-size: 17px;")

        #         layout.addWidget(photoLabel)
        #         layout.addWidget(info)
        #         itemWidget.setLayout(layout)

        #         item.setSizeHint(itemWidget.sizeHint() + QtCore.QSize(50, 30))
        #         self.employeeList.addItem(item)
        #         self.employeeList.setItemWidget(item, itemWidget)
        #         item.setData(QtCore.Qt.ItemDataRole.UserRole, emp)