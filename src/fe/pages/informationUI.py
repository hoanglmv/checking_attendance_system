from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGroupBox, QListWidget, QLineEdit, QListWidgetItem, QGridLayout
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from fe.components.EmployeeHeader import EmployeeHeader
from fe.components.EmployeeSidebar import EmployeeSidebar

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
        self.EmployeeSidebar = EmployeeSidebar(parent=self.centralwidget)
        self.EmployeeSidebar.fil_attendance.setStyleSheet("border-radius: 5px;")
        self.EmployeeSidebar.fil_manage.setStyleSheet("background-color: #68D477; border-radius: 5px;")
        self.horizontalLayout.addWidget(self.EmployeeSidebar)
        
        # Main Container
        self.main = QGroupBox(parent=self.centralwidget)
        self.mainLayout = QVBoxLayout(self.main)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        
        # Header
        self.EmployeeHeader = EmployeeHeader(parent=self.main)

        # Thêm Header vào Main Layout
        self.mainLayout.addWidget(self.EmployeeHeader)

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


        # Tạo các Tab
        self.tab1 = QWidget()  # Tab hiển thị danh sách nhân viên
        self.tab2 = QWidget()  # Tab khác (bạn có thể thay đổi nội dung)

        # Tạo Layout cho nội dung chính trước khi thêm vào tab
        self.contentLayout = QHBoxLayout()
        self.contentLayout.setSpacing(10)

        # Layout cho Tab 1
        self.tab1Layout = QVBoxLayout(self.tab1)
        self.tab1Layout.addLayout(self.contentLayout)  # Giữ nguyên nội dung cũ

        # Nội dung cho Tab 2 (tùy chỉnh)
        self.tab2Layout = QVBoxLayout(self.tab2)
        self.tab2Layout.addWidget(QLabel("Nội dung khác ở đây", alignment=Qt.AlignmentFlag.AlignCenter))

        # Thêm Tab vào TabWidget
        self.tabWidget.addTab(self.tab1, "Thông tin nhân viên")
        self.tabWidget.addTab(self.tab2, "Thêm nhân viên")

        # Thêm TabWidget vào Main Layout
        self.mainLayout.addWidget(self.tabWidget)

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
        
        # Example Employees
        self.employees = [
            {"id": "22022210", "name": "Lê Mai Việt Hoàng", "position": "Leader", "office": "vô gia cư"},
            {"id": "", "name": "", "position": "", "office": ""},
            {"id": "", "name": "", "position": "", "office": ""}
        ]

        for emp in self.employees:
            item = QListWidgetItem()
            itemWidget = QWidget()
            layout = QHBoxLayout(itemWidget)
            layout.setContentsMargins(10, 10, 10, 10)
            layout.setSpacing(50)
            layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            photoLabel = QLabel()
            photoLabel.setFixedSize(80,80)
            photoLabel.setStyleSheet("border-radius: 30px; border: 2px solid white;")


            info = QLabel(f"ID: {emp['id']}\nHọ tên: {emp['name']}\nChức vụ: {emp['position']}\nNơi làm việc: {emp['office']}")
            info.setStyleSheet("color: white; font-size: 17px;")
            
            layout.addWidget(photoLabel)
            layout.addWidget(info)
            itemWidget.setLayout(layout)
            
            item.setSizeHint(itemWidget.sizeHint() + QtCore.QSize(50, 30))
            self.employeeList.addItem(item)
            self.employeeList.setItemWidget(item, itemWidget)
            item.setData(QtCore.Qt.ItemDataRole.UserRole, emp)
        
        self.employeeList.itemClicked.connect(self.displayEmployeeDetails)
        self.contentLayout.addWidget(self.employeeList)

         # Employee Detail
        self.employeeDetail = QGroupBox()
        self.employeeDetail.setStyleSheet("""
        background-color: #0B121F;
        border: 1px solid #68D477;
        padding: 10px;
        border-radius: 10px;
        margin-right: 10px;
    """)

        self.detailLayout = QVBoxLayout(self.employeeDetail)

        # Tạo layout ngang chứa thống kê và ảnh
        self.topLayout = QHBoxLayout()

        # Tạo layout ngang chứa ảnh và thống kê
        self.topLayout = QHBoxLayout()
        self.topLayout.addSpacing(100)  

        # Ảnh nhân viên
        self.photoLabel = QLabel()
        self.photoLabel.setFixedSize(200, 240)
        self.photoLabel.setStyleSheet("border-radius: 8px; border: 2px solid white;")
        self.photoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Thống kê điểm danh
        self.statsLayout = QVBoxLayout()  # Xếp chữ theo chiều dọc
        self.attendanceStats = QLabel("Chuyên cần: ??  \nĐến muộn: ??  \nVề sớm: ??")
        self.attendanceStats.setStyleSheet("color: white; font-size: 18px; border: none;")
        self.attendanceStats.setFixedWidth(200)  # Điều chỉnh kích thước phù hợp
        self.attendanceStats.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.statsLayout.addStretch()  # Đẩy nội dung xuống giữa
        self.statsLayout.addWidget(self.attendanceStats, alignment=Qt.AlignmentFlag.AlignCenter)  # 🌟 Căn giữa
        self.statsLayout.addStretch() 

        # Thêm ảnh trước, thống kê sau (thống kê sẽ nằm bên phải ảnh)
        self.topLayout.addWidget(self.photoLabel) 
        self.topLayout.addSpacing(100) 
        self.topLayout.addLayout(self.statsLayout)  

        # Thông tin nhân viên
        self.infoGrid = QGridLayout()
        labels = ["ID:", "Họ tên:", "Chức vụ:", "Nơi làm việc:", "Email:", "Số điện thoại:"]
        self.lineEdits = {}

        for i, label_text in enumerate(labels):
            label = QLabel(label_text)
            label.setStyleSheet("""
                color: white;
                font-size: 18px;  /* Tăng kích thước chữ */
                font-weight: bold;  /* Làm chữ đậm */
                letter-spacing: 1px;  /* Tạo khoảng cách giữa các chữ */
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
            self.lineEdits[label_text] = line_edit  # Lưu QLineEdit vào từ điển

        # Thêm vào layout chính
        self.detailLayout.addLayout(self.topLayout)  # Đặt ảnh + thống kê lên đầu
        self.detailLayout.addLayout(self.infoGrid)  # Đặt thông tin nhân viên bên dưới

        self.isEditing = False

        # Button Layout
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
        # self.mainLayout.addLayout(self.contentLayout)
        self.horizontalLayout.addWidget(self.main)
        informationUI.setCentralWidget(self.centralwidget)
        
        # Kết nối sự kiện sau khi đã tạo editButton
        self.editButton.clicked.connect(self.toggleEditMode)

    def toggleEditMode(self):
        self.isEditing = not self.isEditing  # Đảo trạng thái chỉnh sửa

        for key in ["ID:", "Họ tên:", "Chức vụ:", "Nơi làm việc:", "Email:", "Số điện thoại:"]:
            self.lineEdits[key].setReadOnly(not self.isEditing)  # Cho phép chỉnh sửa nếu đang ở chế độ chỉnh sửa

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
            # Lưu dữ liệu vào danh sách nhân viên
            selected_item = self.employeeList.currentItem()
            if selected_item:
                emp = selected_item.data(QtCore.Qt.ItemDataRole.UserRole)
                emp["id"] = self.lineEdits["ID:"].text()
                emp["name"] = self.lineEdits["Họ tên:"].text()
                emp["position"] = self.lineEdits["Chức vụ:"].text()
                emp["office"] = self.lineEdits["Nơi làm việc:"].text()

                # KHÔNG CẬP NHẬT EMAIL & SĐT vào danh sách
                new_text = f"ID: {emp['id']}\nHọ tên: {emp['name']}\nChức vụ: {emp['position']}\nNơi làm việc: {emp['office']}"
                
                itemWidget = QWidget()
                layout = QHBoxLayout(itemWidget)
                layout.setContentsMargins(10, 10, 10, 10)
                layout.setSpacing(50)
                layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

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

    #Tab2
    


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    informationUI = QtWidgets.QMainWindow()
    ui = Ui_informationUI()
    ui.setupUi(informationUI)
    informationUI.show()
    sys.exit(app.exec())
