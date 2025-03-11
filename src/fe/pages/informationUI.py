from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGroupBox, QListWidget, QLineEdit, QListWidgetItem, QGridLayout

import sys
import os

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

        # Thêm Header vào Main Layout
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


        # Tạo các Tab
        self.tab1 = QWidget()  # Tab hiển thị danh sách nhân viên
        self.tab2 = QWidget()  # Tab khác (bạn có thể thay đổi nội dung)

        # Tạo Layout cho nội dung chính trước khi thêm vào tab
        self.contentLayout = QHBoxLayout()
        self.contentLayout.setSpacing(10)
        
        # Thêm TabWidget vào Main Layout
        self.mainLayout.addWidget(self.tabWidget)
            
        # Layout cho Tab 1
        self.tab1Layout = QVBoxLayout(self.tab1)
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

##-------------------------------------------------------------------------------##
        # Tab 2 - Thêm Nhân Viên
        self.tab2 = QWidget()
        self.tabWidget.addTab(self.tab2, "Thêm nhân viên")

        # Layout ngang chính cho tab2
        self.tab2Layout = QHBoxLayout(self.tab2)
        self.tab2Layout.setContentsMargins(20, 10, 20, 20)
        self.tab2Layout.setSpacing(40)
 
        self.leftLayout = QVBoxLayout()
        self.leftLayout.setSpacing(20)
        self.leftLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.leftLayout.setContentsMargins(50, 0, 0, 0)
        

        # Ảnh camera (giả lập ảnh tròn, viền trắng)
        self.cameraLabel = QLabel()
        self.cameraLabel.setFixedSize(350, 450)
        self.cameraLabel.setStyleSheet("border-radius: 175px; border: 2px solid white;")
        self.cameraLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # (Tuỳ chọn) Nếu muốn hiển thị ảnh có sẵn:
        # pixmap = QPixmap("path/to/your_image.jpg").scaled(
        #     self.cameraLabel.width(),
        #     self.cameraLabel.height(),
        #     Qt.AspectRatioMode.KeepAspectRatio,
        #     Qt.TransformationMode.SmoothTransformation
        # )
        # self.cameraLabel.setPixmap(pixmap)

        self.leftLayout.addWidget(self.cameraLabel)

        # Label hướng dẫn
        self.instructionLabel = QLabel("Vui lòng căn chỉnh khuôn mặt của bạn \nvào giữa và nhìn thẳng vào khung hình  ")
        self.instructionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instructionLabel.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        self.leftLayout.addWidget(self.instructionLabel)

        # Thêm layout trái vào tab2Layout
        self.tab2Layout.addLayout(self.leftLayout)

        # Tạo một QGroupBox để chứa bố cục chi tiết
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

        # Layout dọc chính bên trong groupBox
        self.addDetailLayout = QVBoxLayout(self.addEmployeeDetail)

        self.topLayout2 = QHBoxLayout()
        self.topLayout2.addSpacing(100)

        # Ảnh bên phải
        self.photoLabel2 = QLabel()
        self.photoLabel2.setFixedSize(180, 216)
        self.photoLabel2.setStyleSheet("border-radius: 8px; border: 2px solid white;")
        self.photoLabel2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Thống kê điểm danh
        self.statsLayout2 = QVBoxLayout()
        self.attendanceStats2 = QLabel("Chuyên cần: ??\nĐến muộn: ??\nVề sớm: ??")
        self.attendanceStats2.setStyleSheet("color: white; font-size: 18px; border: none;")
        self.attendanceStats2.setFixedWidth(200)
        self.attendanceStats2.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.statsLayout2.addStretch()
        self.statsLayout2.addWidget(self.attendanceStats2, alignment=Qt.AlignmentFlag.AlignCenter)
        self.statsLayout2.addStretch()

        # Thêm 2 khối vào topLayout2
        self.topLayout2.addWidget(self.photoLabel2)
        self.topLayout2.addSpacing(100)
        self.topLayout2.addLayout(self.statsLayout2)

        # Đưa topLayout2 vào layout dọc
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
            line_edit.setReadOnly(False)  # Mở để nhập thông tin mới

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

        # Tạo layout dọc bên phải để đặt groupBox
        self.rightLayout = QVBoxLayout()
        self.rightLayout.addWidget(self.addEmployeeDetail)

        # Thêm layout bên phải vào tab2Layout
        self.tab2Layout.addLayout(self.rightLayout)

##-------------------------------------------------------------------------------##
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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    informationUI = QtWidgets.QMainWindow()
    ui = Ui_informationUI()
    ui.setupUi(informationUI)
    informationUI.show()
    sys.exit(app.exec())
