import csv
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGroupBox, QListWidget, QLineEdit, QListWidgetItem, QGridLayout
import sys
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from fe.components.header import Header
from fe.components.sidebar import Sidebar

class Ui_informationUI(object):
    def setupUi(self, informationUI):
        informationUI.setObjectName("informationUI")
        informationUI.resize(1560, 800)
        informationUI.setStyleSheet("background-color: #0B121F; border: none;")
        
        self.centralwidget = QtWidgets.QWidget(parent=informationUI)
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        
        # Sidebar
        self.sidebar = Sidebar(parent=self.centralwidget)
        self.sidebar.fil_attendance.setStyleSheet("border-radius: 5px;")
        self.sidebar.fil_manage.setStyleSheet("background-color: #68D477; border-radius: 5px;")
        self.horizontalLayout.addWidget(self.sidebar)
        
        # Main Container
        self.main = QGroupBox(parent=self.centralwidget)
        self.mainLayout = QVBoxLayout(self.main)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        
        # Header
        self.header = Header(parent=self.main)
        self.mainLayout.addWidget(self.header)

        # Tạo Tab Widget
        self.tabWidget = QtWidgets.QTabWidget()
        self.tabWidget.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #1E2A38;
                background: #0B121F;
                border-radius: 10px;
            }
            QTabBar::tab {
                background: #1E2A38;
                color: white;
                padding: 12px 20px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                margin: 4px;
                transition: all 0.3s ease-in-out;
            }
            QTabBar::tab:selected {
                background: #68D477;
                color: black;
                border-bottom: 3px solid #4CAF50;
                font-size: 15px;
            }
            QTabBar::tab:hover {
                background: #2E3A4E;
                color: #A4F9C8;
            }
            QTabBar::tab:!selected {
                background: #11203B;
                color: #C0C0C0;
            }
        """)
        self.mainLayout.addWidget(self.tabWidget)
        
        # Tab 1: Thông tin nhân viên
        self.tab1 = QWidget()
        self.tab1Layout = QVBoxLayout(self.tab1)
        self.contentLayout = QHBoxLayout()
        self.contentLayout.setSpacing(10)
        self.tab1Layout.addLayout(self.contentLayout)
        self.tabWidget.addTab(self.tab1, "Thông tin nhân viên")
        
        # Employee List
        self.employeeList = QListWidget()
        self.employeeList.setStyleSheet("""
            QListWidget {
                background-color: #0B121F;
                border: none;
            }
            QListWidget::item {
                background-color: #11203B;
                border: 1px solid #5A6986;
                border-radius: 8px;
                padding:4px;
                margin: 10px;
                color: white;
                font-size: 12px;
            }
            QListWidget::item:selected {
                border: 2px solid #68D477;
                background-color: #0F2A47;
            }
        """)
        self.employeeList.setFixedWidth(450)
        self.employeeList.itemClicked.connect(self.displayEmployeeDetails)
        self.contentLayout.addWidget(self.employeeList)
        
        # Employee Detail (phần hiển thị thông tin chi tiết nhân viên)
        self.employeeDetail = QGroupBox()
        self.employeeDetail.setStyleSheet("""
            background-color: #0B121F;
            border: 1px solid #68D477;
            padding: 10px;
            border-radius: 10px;
            margin-right: 10px;
        """)
        self.detailLayout = QVBoxLayout(self.employeeDetail)
        self.topLayout = QHBoxLayout()
        self.topLayout.addSpacing(100)
        self.photoLabel = QLabel()
        self.photoLabel.setFixedSize(200, 240)
        self.photoLabel.setStyleSheet("border-radius: 8px; border: 2px solid white;")
        self.photoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.statsLayout = QVBoxLayout()
        self.attendanceStats = QLabel("Chuyên cần: ??  \nĐến muộn: ??  \nVề sớm: ??")
        self.attendanceStats.setStyleSheet("color: white; font-size: 18px; border: none;")
        self.attendanceStats.setFixedWidth(200)
        self.attendanceStats.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.statsLayout.addStretch()
        self.statsLayout.addWidget(self.attendanceStats, alignment=Qt.AlignmentFlag.AlignCenter)
        self.statsLayout.addStretch()
        self.topLayout.addWidget(self.photoLabel)
        self.topLayout.addSpacing(100)
        self.topLayout.addLayout(self.statsLayout)
        self.infoGrid = QGridLayout()
        labels = ["ID:", "Họ tên:", "Chức vụ:", "Nơi làm việc:", "Email:", "Số điện thoại:"]
        self.lineEdits = {}
        for i, label_text in enumerate(labels):
            label = QLabel(label_text)
            label.setStyleSheet("""
                color: white;
                font-size: 18px;
                font-weight: bold;
                letter-spacing: 1px;
            """)
            line_edit = QLineEdit()
            line_edit.setStyleSheet("""
                background-color: white;
                color: black;
                font-size: 16px;
                padding: 5px;
                border-radius: 5px;
            """)
            line_edit.setReadOnly(True)
            self.infoGrid.addWidget(label, i, 0)
            self.infoGrid.addWidget(line_edit, i, 1)
            self.lineEdits[label_text] = line_edit
        self.detailLayout.addLayout(self.topLayout)
        self.detailLayout.addLayout(self.infoGrid)
        self.isEditing = False
        self.buttonLayout = QHBoxLayout()
        self.deleteButton = QPushButton("Xóa nhân viên")
        self.deleteButton.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: darkred;
            }
        """)
        self.editButton = QPushButton("Thay đổi thông tin")
        self.editButton.setStyleSheet("""
            QPushButton {
                background-color: #68D477;
                color: black;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #5AC469;
            }
        """)
        self.buttonLayout.addWidget(self.deleteButton)
        self.buttonLayout.addWidget(self.editButton)
        self.detailLayout.addLayout(self.buttonLayout)
        self.contentLayout.addWidget(self.employeeDetail)
        self.horizontalLayout.addWidget(self.main)
        informationUI.setCentralWidget(self.centralwidget)
        self.editButton.clicked.connect(self.toggleEditMode)
        
        # Tab 2: Thêm nhân viên (tương tự như code gốc)
        self.tab2 = QWidget()
        self.tabWidget.addTab(self.tab2, "Thêm nhân viên")
        self.tab2Layout = QHBoxLayout(self.tab2)
        self.tab2Layout.setContentsMargins(20, 10, 20, 20)
        self.tab2Layout.setSpacing(40)
        self.leftLayout = QVBoxLayout()
        self.leftLayout.setSpacing(20)
        self.leftLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.leftLayout.setContentsMargins(50, 0, 0, 0)
        self.cameraLabel = QLabel()
        self.cameraLabel.setFixedSize(350, 450)
        self.cameraLabel.setStyleSheet("border-radius: 175px; border: 2px solid white;")
        self.cameraLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.leftLayout.addWidget(self.cameraLabel)
        self.instructionLabel = QLabel("Vui lòng căn chỉnh khuôn mặt của bạn \nvào giữa và nhìn thẳng vào khung hình  ")
        self.instructionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instructionLabel.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        self.leftLayout.addWidget(self.instructionLabel)
        self.tab2Layout.addLayout(self.leftLayout)
        self.addEmployeeDetail = QGroupBox()
        self.addEmployeeDetail.setStyleSheet("""
            QGroupBox {
                background-color: #0B121F;
                border: 1px solid #68D477;
                padding: 10px;
                border-radius: 10px;
                margin-right: 10px;
            }
        """)
        self.addDetailLayout = QVBoxLayout(self.addEmployeeDetail)
        self.topLayout2 = QHBoxLayout()
        self.topLayout2.addSpacing(100)
        self.photoLabel2 = QLabel()
        self.photoLabel2.setFixedSize(180, 216)
        self.photoLabel2.setStyleSheet("border-radius: 8px; border: 2px solid white;")
        self.photoLabel2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.statsLayout2 = QVBoxLayout()
        self.attendanceStats2 = QLabel("Chuyên cần: ??\nĐến muộn: ??\nVề sớm: ??")
        self.attendanceStats2.setStyleSheet("color: white; font-size: 18px; border: none;")
        self.attendanceStats2.setFixedWidth(200)
        self.attendanceStats2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.statsLayout2.addStretch()
        self.statsLayout2.addWidget(self.attendanceStats2, alignment=Qt.AlignmentFlag.AlignCenter)
        self.statsLayout2.addStretch()
        self.topLayout2.addWidget(self.photoLabel2)
        self.topLayout2.addSpacing(100)
        self.topLayout2.addLayout(self.statsLayout2)
        self.addDetailLayout.addLayout(self.topLayout2)
        self.infoGrid2 = QGridLayout()
        labels_tab2 = ["ID:", "Họ tên:", "Chức vụ:", "Nơi làm việc:", "Email:", "Số điện thoại:"]
        self.newLineEdits = {}
        for i, label_text in enumerate(labels_tab2):
            label = QLabel(label_text)
            label.setStyleSheet("""
                color: white;
                font-size: 18px;
                font-weight: bold;
                letter-spacing: 1px;
            """)
            line_edit = QLineEdit()
            line_edit.setStyleSheet("""
                background-color: white;
                color: black;
                font-size: 16px;
                padding: 5px;
                border-radius: 5px;
            """)
            line_edit.setReadOnly(False)
            self.infoGrid2.addWidget(label, i, 0)
            self.infoGrid2.addWidget(line_edit, i, 1)
            self.newLineEdits[label_text] = line_edit
        self.addDetailLayout.addLayout(self.infoGrid2)
        self.buttonLayout2 = QHBoxLayout()
        self.buttonLayout2.addStretch()
        self.saveButton2 = QPushButton("Lưu thông tin")
        self.saveButton2.setStyleSheet("""
            QPushButton {
                background-color: #68D477;
                color: black;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #5AC469;
            }
        """)
        self.buttonLayout2.addWidget(self.saveButton2)
        self.buttonLayout2.addStretch()
        self.addDetailLayout.addLayout(self.buttonLayout2)
        self.rightLayout = QVBoxLayout()
        self.rightLayout.addWidget(self.addEmployeeDetail)
        self.tab2Layout.addLayout(self.rightLayout)

        # Sau khi xây dựng giao diện, thay vì dùng dữ liệu cứng, load dữ liệu từ file:
        self.employees = self.load_employees_from_csv("employees.csv")
        self.populate_employee_list()

        # Kết nối sự kiện nút lưu ở tab2 (nếu bạn muốn thêm nhân viên mới từ tab này)
        self.saveButton2.clicked.connect(self.add_new_employee)

    # ------------------- Các hàm tổng quát -------------------# ------------------- Các hàm tổng quát -------------------

<<<<<<< kien
    def load_employees_from_file(self,file_path):
        """Load dữ liệu nhân viên từ file JSON, tạo file nếu chưa tồn tại."""
        if not os.path.exists(file_path):
            print(f"File {file_path} không tồn tại, tạo file mới...")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump({"employees": []}, f, ensure_ascii=False, indent=4)  # Ghi dữ liệu rỗng vào file

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data.get("employees", [])
        except json.JSONDecodeError:
            print(f"Lỗi đọc file {file_path}, tạo dữ liệu mới...")
            return []
=======
    def load_employees_from_csv(self, file_path):
        employees = []
        try:
            with open(file_path, mode='r', encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    # Giả sử file CSV có header: id, name, position, office, email, phone
                    employees.append({
                        "id": row.get("id", ""),
                        "name": row.get("name", ""),
                        "position": row.get("position", ""),
                        "office": row.get("office", ""),
                        "email": row.get("email", ""),
                        "phone": row.get("phone", "")
                    })
        except Exception as e:
            print("Lỗi khi load dữ liệu từ CSV:", e)
        return employees

>>>>>>> main
    def populate_employee_list(self):
        """Xóa danh sách cũ và thêm lại các mục nhân viên từ self.employees."""
        self.employeeList.clear()
        for emp in self.employees:
            self.add_employee_to_list(emp)

    def add_employee_to_list(self, emp):
        """
        Tạo widget cho một nhân viên và thêm vào QListWidget.
        Dữ liệu emp là dictionary chứa các thông tin: id, name, position, office.
        """
        item = QListWidgetItem()
        itemWidget = QWidget()
        layout = QHBoxLayout(itemWidget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(50)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        
        photoLabel = QLabel()
        photoLabel.setFixedSize(80, 80)
        photoLabel.setStyleSheet("border-radius: 30px; border: 2px solid white;")
        
        info_text = (
            f"ID: {emp.get('id', '')}\n"
            f"Họ tên: {emp.get('name', '')}\n"
            f"Chức vụ: {emp.get('position', '')}\n"
            f"Nơi làm việc: {emp.get('office', '')}"
        )
        info = QLabel(info_text)
        info.setStyleSheet("color: white; font-size: 17px;")
        
        layout.addWidget(photoLabel)
        layout.addWidget(info)
        itemWidget.setLayout(layout)
        
        item.setSizeHint(itemWidget.sizeHint() + QtCore.QSize(50, 30))
        self.employeeList.addItem(item)
        self.employeeList.setItemWidget(item, itemWidget)
        item.setData(QtCore.Qt.ItemDataRole.UserRole, emp)

    import csv

    def add_new_employee(self, file_path):
        new_emp = {
            "id": self.newLineEdits["ID:"].text(),
            "name": self.newLineEdits["Họ tên:"].text(),
            "position": self.newLineEdits["Chức vụ:"].text(),
            "office": self.newLineEdits["Nơi làm việc:"].text(),
            "email": self.newLineEdits["Email:"].text(),
            "phone": self.newLineEdits["Số điện thoại:"].text()
        }

        # Kiểm tra dữ liệu bắt buộc
        if not new_emp["id"] or not new_emp["name"]:
            print("Vui lòng nhập đầy đủ ID và Họ tên!")
            return

        # Cập nhật thông tin chi tiết nhân viên trong tab thông tin
        self.lineEdits["ID:"].setText(new_emp["id"])
        self.lineEdits["Họ tên:"].setText(new_emp["name"])
        self.lineEdits["Chức vụ:"].setText(new_emp["position"])
        self.lineEdits["Nơi làm việc:"].setText(new_emp["office"])
        self.lineEdits["Email:"].setText(new_emp["email"])
        self.lineEdits["Số điện thoại:"].setText(new_emp["phone"])

        # Chuyển tab về "Thông tin nhân viên" (index = 0)
        self.tabWidget.setCurrentIndex(0)

        # Thêm nhân viên mới vào danh sách chung và cập nhật giao diện
        self.employees.append(new_emp)
        self.add_employee_to_list(new_emp)

        # Lưu danh sách nhân viên vào file CSV
        fieldnames = ["id", "name", "position", "office", "email", "phone"]
        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                for emp in self.employees:
                    writer.writerow(emp)
        except Exception as e:
            print("Lỗi khi lưu dữ liệu vào file CSV:", e)

        # Xóa dữ liệu nhập ở tab "Thêm nhân viên" sau khi lưu
        for line_edit in self.newLineEdits.values():
            line_edit.clear()

    def toggleEditMode(self):
        self.isEditing = not self.isEditing  # Đảo trạng thái chỉnh sửa

        for key in ["ID:", "Họ tên:", "Chức vụ:", "Nơi làm việc:", "Email:", "Số điện thoại:"]:
            self.lineEdits[key].setReadOnly(not self.isEditing)

        if self.isEditing:
            self.editButton.setText("Lưu thay đổi")
            self.editButton.setStyleSheet("""
                QPushButton {
                    background-color: #FFA500;
                    color: black;
                    padding: 10px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #E69500;
                }
            """)
        else:
            # Khi lưu thay đổi
            selected_item = self.employeeList.currentItem()
            if selected_item:
                emp = selected_item.data(QtCore.Qt.ItemDataRole.UserRole)
                emp["id"] = self.lineEdits["ID:"].text()
                emp["name"] = self.lineEdits["Họ tên:"].text()
                emp["position"] = self.lineEdits["Chức vụ:"].text()
                emp["office"] = self.lineEdits["Nơi làm việc:"].text()
                emp["email"] = self.lineEdits["Email:"].text()
                emp["phone"] = self.lineEdits["Số điện thoại:"].text()

                new_text = (
                    f"ID: {emp['id']}\n"
                    f"Họ tên: {emp['name']}\n"
                    f"Chức vụ: {emp['position']}\n"
                    f"Nơi làm việc: {emp['office']}"
                )

                itemWidget = QWidget()
                layout = QHBoxLayout(itemWidget)
                layout.setContentsMargins(10, 10, 10, 10)
                layout.setSpacing(50)
                layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                photoLabel = QLabel()
                photoLabel.setFixedSize(80, 80)
                photoLabel.setStyleSheet("border-radius: 30px; border: 2px solid white;")

                info = QLabel(new_text)
                info.setStyleSheet("color: white; font-size: 17px;")

                layout.addWidget(photoLabel)
                layout.addWidget(info)
                itemWidget.setLayout(layout)

                selected_item.setSizeHint(itemWidget.sizeHint() + QtCore.QSize(50, 30))
                self.employeeList.setItemWidget(selected_item, itemWidget)
                selected_item.setData(QtCore.Qt.ItemDataRole.UserRole, emp)

            self.editButton.setText("Thay đổi thông tin")
            self.editButton.setStyleSheet("""
                QPushButton {
                    background-color: #68D477;
                    color: black;
                    padding: 10px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #5AC469;
                }
            """)
    
    def displayEmployeeDetails(self, item):
        emp = item.data(QtCore.Qt.ItemDataRole.UserRole)
        self.lineEdits["ID:"].setText(emp['id'])
        self.lineEdits["Họ tên:"].setText(emp['name'])
        self.lineEdits["Chức vụ:"].setText(emp['position'])
        self.lineEdits["Nơi làm việc:"].setText(emp['office'])
        self.lineEdits["Email:"].setText(emp.get('email', ''))
        self.lineEdits["Số điện thoại:"].setText(emp.get('phone', ''))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    informationUI = QtWidgets.QMainWindow()
    ui = Ui_informationUI()
    ui.setupUi(informationUI)
    informationUI.show()
    sys.exit(app.exec())
