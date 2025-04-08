from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QWidget, QHeaderView, QAbstractItemView, QTableWidgetItem, QHBoxLayout, QCheckBox, QDateEdit, QLabel, QLineEdit
from PyQt6.QtCore import pyqtSignal, QObject, QDate
import sys
import os
import requests
from datetime import datetime
from PyQt6.QtCore import QSettings

# Cấu hình encoding UTF-8
sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from fe.components.header import Header
from fe.components.sidebar import Sidebar

class Ui_checkingUI(object):
    def setupUi(self, checkingUI):
        checkingUI.setObjectName("checkingUI")
        checkingUI.resize(1560, 610)
        checkingUI.setStyleSheet("background-color: #0B121F; border: none;")
        
        self.centralwidget = QtWidgets.QWidget(parent=checkingUI)
        self.centralwidget.setObjectName("centralwidget")
        
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        
        self.sidebar = Sidebar(parent=self.centralwidget)
        self.sidebar.fil_attendance.setStyleSheet("background-color: #68D477; border-radius: 5px;")
        self.sidebar.fil_manage.setStyleSheet("background-color: #1B2B40; border-radius: 5px;")
        self.horizontalLayout.addWidget(self.sidebar)       
        
        self.main = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.main.setObjectName("main")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.main)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)   
        
        self.header = Header(parent=self.main)
        self.verticalLayout.addWidget(self.header)     
        
        self.groupBox = QtWidgets.QGroupBox(parent=self.main)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 60))
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 60))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")

        # Sử dụng QHBoxLayout để chứa hai nút
        self.button_layout = QtWidgets.QHBoxLayout(self.groupBox)
        self.button_layout.setContentsMargins(10, 10, 10, 10)  # Thêm lề để không sát viền
        self.button_layout.setSpacing(10)  # Khoảng cách giữa hai nút

        # Nút "Điểm danh theo ngày"
        self.btn_day_attendance = QtWidgets.QPushButton(parent=self.groupBox)
        self.btn_day_attendance.setMinimumSize(QtCore.QSize(180, 40))  # Tăng kích thước để chữ không bị vướng
        self.btn_day_attendance.setMaximumSize(QtCore.QSize(180, 40))
        self.btn_day_attendance.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #68D477, stop:1 #4CAF50);
                color: black;
                padding: 10px 20px;  
                border-radius: 6px;
                font-size: 13px;  
                font-weight: 600;
                border-bottom: 2px solid #4CAF50;
                transition: all 0.3s ease;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #7BEF88, stop:1 #5CBF60);
                color: black;
                box-shadow: 0 2px 4px rgba(104, 212, 119, 0.5);
                transform: scale(1.05);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #68D477, stop:1 #4CAF50);
                color: black;
                border-bottom: 2px solid #4CAF50;
            }
        """)
        self.btn_day_attendance.setText("Điểm danh theo ngày")
        self.btn_day_attendance.setObjectName("btn_day_attendance")
        self.btn_day_attendance.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.button_layout.addWidget(self.btn_day_attendance)

        # Nút "Điểm danh theo tháng"
        self.btn_month_attendance = QtWidgets.QPushButton(parent=self.groupBox)
        self.btn_month_attendance.setMinimumSize(QtCore.QSize(180, 40))  
        self.btn_month_attendance.setMaximumSize(QtCore.QSize(180, 40))
        self.btn_month_attendance.setStyleSheet("""
            QPushButton {
                background: #1E2A38;
                color: #C0C0C0;
                padding: 10px 20px;  
                border-radius: 6px;
                font-size: 13px;  
                font-weight: 600;
                transition: all 0.3s ease;
            }
            QPushButton:hover {
                background: #2E3A4E;
                color: #A4F9C8;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
                transform: scale(1.05);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #68D477, stop:1 #4CAF50);
                color: black;
                border-bottom: 2px solid #4CAF50;
            }
        """)
        self.btn_month_attendance.setText("Điểm danh theo tháng")
        self.btn_month_attendance.setObjectName("btn_month_attendance")
        self.btn_month_attendance.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.button_layout.addWidget(self.btn_month_attendance)

        self.button_layout.addStretch()

        self.verticalLayout.addWidget(self.groupBox)
        
        self.stas_time = QtWidgets.QGroupBox(parent=self.main)
        self.stas_time.setMinimumSize(QtCore.QSize(0, 75))
        self.stas_time.setMaximumSize(QtCore.QSize(16777215, 75))
        self.stas_time.setStyleSheet("background-color: #192E44; margin-bottom: 5px;")
        self.stas_time.setTitle("")
        self.stas_time.setObjectName("stas_time")
        self.verticalLayout.addWidget(self.stas_time)
        
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.stas_time)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        
        self.horizontalLayout_2.addSpacing(20)
        
        # Thêm nhãn "Chọn ngày"
        self.date_label = QLabel("Chọn ngày:", parent=self.stas_time)
        self.date_label.setStyleSheet("color: white; font: 9pt \"Times New Roman\";")
        self.horizontalLayout_2.addWidget(self.date_label)

        # Cải thiện giao diện QDateEdit
        self.date_edit = QDateEdit(parent=self.stas_time)
        self.date_edit.setMinimumSize(QtCore.QSize(150, 30))
        self.date_edit.setMaximumSize(QtCore.QSize(150, 30))
        self.date_edit.setStyleSheet("""
            QDateEdit {
                border: 2px solid #9FEF00;
                border-radius: 5px;
                color: white;
                font: 9pt "Times New Roman";
                background-color: #2E3A4E;
                padding: 5px;
                transition: all 0.3s ease;
            }
            QDateEdit:hover {
                border: 2px solid #A4F9C8;
                background-color: #3E4A5E;
                box-shadow: 0 2px 4px rgba(164, 249, 200, 0.3);
            }
            QDateEdit:focus {
                border: 2px solid #68D477;
                background-color: #3E4A5E;
                box-shadow: 0 2px 4px rgba(104, 212, 119, 0.5);
            }
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #9FEF00;
                border-left-style: solid;
            }
            QDateEdit::down-arrow {
                image: url(src/fe/Image_and_icon/icons8-calendar-20.png);
            }
            QCalendarWidget {
                background-color: #2E3A4E;
                color: white;
            }
            QCalendarWidget QToolButton {
                color: white;
                background-color: #3E4A5E;
                border: none;
            }
            QCalendarWidget QToolButton:hover {
                background-color: #68D477;
            }
            QCalendarWidget QMenu {
                background-color: #2E3A4E;
                color: white;
            }
            QCalendarWidget QMenu::item:selected {
                background-color: #68D477;
            }
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background-color: #192E44;
            }
            QCalendarWidget QAbstractItemView {
                background-color: #2E3A4E;
                color: white;
                selection-background-color: #68D477;
                selection-color: black;
            }
        """)
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setObjectName("date_edit")
        self.date_edit.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

        line_edit = QLineEdit(self.date_edit)
        line_edit.setReadOnly(True)
        self.date_edit.setLineEdit(line_edit)

        self.horizontalLayout_2.addWidget(self.date_edit)
        
        self.horizontalLayout_2.addStretch()
        
        self.btn_total = self.create_btn(self.stas_time, "Tất cả", 0)
        self.btn_total.setObjectName("btn_total")
        self.horizontalLayout_2.addWidget(self.btn_total)

        self.horizontalLayout_2.addSpacing(10)
        
        self.btn_late = self.create_btn(self.stas_time, "Muộn", 0)
        self.btn_late.setObjectName("btn_late")
        self.horizontalLayout_2.addWidget(self.btn_late)
        
        self.horizontalLayout_2.addSpacing(10)
        
        self.btn_cp = self.create_btn(self.stas_time, "Có phép", 0)
        self.btn_cp.setObjectName("btn_cp")
        self.horizontalLayout_2.addWidget(self.btn_cp)
        
        self.horizontalLayout_2.addSpacing(10)
        
        self.btn_kp = self.create_btn(self.stas_time, "Không phép", 0)
        self.btn_kp.setObjectName("btn_kp")
        self.horizontalLayout_2.addWidget(self.btn_kp)
        
        self.horizontalLayout_2.addSpacing(20)
         
        self.content = QtWidgets.QGroupBox(parent=self.main)
        self.content.setStyleSheet("background-color: #192E44; border-radius: 8px;")
        self.content.setTitle("")
        self.content.setObjectName("content")
        
        self.table = QtWidgets.QTableWidget(self.content)
        self.table.setColumnCount(8)

        self.table.setHorizontalHeaderLabels(["Mã nhân viên", "Họ và tên", "Chức vụ", "Muộn", "Giờ đến", "Giờ về", "Nghỉ có phép", "Nghỉ không phép"])

        self.table.setColumnWidth(0, 100)  
        self.table.setColumnWidth(2, 300) 
        self.table.setColumnWidth(3, 60) 
        self.table.setColumnWidth(4, 100) 
        self.table.setColumnWidth(5, 100) 
        self.table.setColumnWidth(6, 100) 
        self.table.setColumnWidth(7, 120) 

        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeMode.Fixed)

        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #1E2A38;
                color: white;
                border: 2px solid #9FEF00;
                border-radius: 8px;
                gridline-color: #4A5A6E;
                font: 9pt "Times New Roman";
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            }
            QHeaderView::section {
                background-color: #192E44;
                color: #A4F9C8;
                font-weight: bold;
                padding: 8px;
                border: 1px solid #9FEF00;
                border-bottom: 2px solid #68D477;
            }
            QTableWidget::item {
                background-color: #1E2A38;
                color: white;
                padding: 0px;  /* Loại bỏ padding */
                border: 1px solid #4A5A6E;
                transition: all 0.3s ease;
            }
            QTableWidget::item:hover {
                background-color: #2E3A4E;
                color: #A4F9C8;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            }
            QTableWidget::item:selected {
                background-color: #68D477;
                color: black;
                box-shadow: 0 2px 4px rgba(104, 212, 119, 0.5);
            }
            QTableWidget QTableCornerButton::section {
                background-color: #192E44;
                border: 1px solid #9FEF00;
            }
            QTableWidget::verticalScrollBar {
                background: #0B121F;
                width: 10px;
                margin: 0px;
                border-radius: 5px;
            }
            QTableWidget::verticalScrollBar::handle {
                background: #68D477;
                border-radius: 5px;
                min-height: 20px;
            }
            QTableWidget::verticalScrollBar::handle:hover {
                background: #5AC469;
            }
            QTableWidget::verticalScrollBar::add-line, QTableWidget::verticalScrollBar::sub-line {
                background: none;
                height: 0px;
            }
            QTableWidget::verticalScrollBar::add-page, QTableWidget::verticalScrollBar::sub-page {
                background: none;
            }
        """)
        
        self.table.horizontalHeader().setVisible(True)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.verticalHeader().setVisible(False)

        layout = QtWidgets.QVBoxLayout(self.content)
        layout.addWidget(self.table)
        self.content.setLayout(layout)
        
        self.verticalLayout.addWidget(self.content)
        self.horizontalLayout.addWidget(self.main)
        
        checkingUI.setCentralWidget(self.centralwidget)
        
        # Kết nối sự kiện thay đổi checkbox
        self.table.itemChanged.connect(self.on_checkbox_changed)

    def retranslateUi(self, checkingUI):
        _translate = QtCore.QCoreApplication.translate
        checkingUI.setWindowTitle(_translate("checkingUI", "MainWindow"))
        
    def create_btn(self, pr, status, count):
        button = QtWidgets.QPushButton(parent=pr)
        button.setMinimumSize(QtCore.QSize(100, 30))
        button.setMaximumSize(QtCore.QSize(100, 30))        
        button.setStyleSheet("""
            QPushButton {
                border: 2px solid #9FEF00;
                border-radius: 5px;
                color: white;
                font: 9pt "Times New Roman";
                background-color: #2E3A4E;
                padding: 5px;
                transition: all 0.3s ease;
            }
            QPushButton:hover {
                border: 2px solid #A4F9C8;
                background-color: #3E4A5E;
                color: #A4F9C8;
                box-shadow: 0 2px 4px rgba(164, 249, 200, 0.3);
                transform: scale(1.05);
            }
            QPushButton:pressed {
                border: 2px solid #68D477;
                background-color: #3E4A5E;
                color: #68D477;
                box-shadow: 0 2px 4px rgba(104, 212, 119, 0.5);
            }
        """)
        button.setText(f"{status}: {count}")
        button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        return button

    def load_attendance_data(self, date=None):
        if date is None:
            date = self.date_edit.date().toString("yyyy-MM-dd")
        else:
            # Cập nhật QDateEdit để hiển thị ngày được truyền vào
            selected_date = QDate.fromString(date, "yyyy-MM-dd")
            self.date_edit.setDate(selected_date)
            print(f"Đặt ngày trong QDateEdit: {date}")

        settings = QSettings("MyApp", "LoginApp")
        token = settings.value("access_token", None)
        if not token:
            print("Không có token, không thể tải dữ liệu điểm danh")
            QtWidgets.QMessageBox.warning(self.centralwidget, "Lỗi", "Không có token, vui lòng đăng nhập lại.")
            return False

        headers = {"Authorization": f"Bearer {token}"}
        url = f"http://127.0.0.1:8000/attendance/daily?date={date}"
        print(f"Gọi API tải dữ liệu: {url}")
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            self.table.setRowCount(0)
            total_employees = data["summary"]["total_employees"]
            total_late = data["summary"]["total_late"]
            total_absent_with_permission = data["summary"]["total_absent_with_permission"]
            total_absent_without_permission = data["summary"]["total_absent_without_permission"]

            self.btn_total.setText(f"Tất cả: {total_employees}")
            self.btn_late.setText(f"Muộn: {total_late}")
            self.btn_cp.setText(f"Có phép: {total_absent_with_permission}")
            self.btn_kp.setText(f"Không phép: {total_absent_without_permission}")

            # Kiểm tra xem có dữ liệu nhân viên không
            if not data["departments"]:
                print("Không có dữ liệu nhân viên cho ngày này")
                QtWidgets.QMessageBox.information(self.centralwidget, "Thông báo", f"Không có dữ liệu điểm danh cho ngày {date}.")
                return True

            for department, employees in data["departments"].items():
                for emp in employees:
                    self.add_row(
                        emp["employee_code"],
                        emp["employee_id"],
                        emp["full_name"],
                        emp["position"],
                        emp["late"],
                        emp["check_in_time"] if emp["check_in_time"] else "",
                        "",
                        emp["absent_with_permission"],
                        emp["absent_without_permission"]
                    )
            return True
        except requests.RequestException as e:
            print(f"Lỗi khi tải dữ liệu điểm danh: {str(e)}")
            QtWidgets.QMessageBox.warning(self.centralwidget, "Lỗi", f"Lỗi khi tải dữ liệu điểm danh: {str(e)}")
            return False

    def add_row(self, employee_code, employee_id, name, role, late, time_in, time_out, cp, kp):
        row_count = self.table.rowCount()
        self.table.setRowCount(row_count + 1)

        # Hiển thị employee_code trong cột "Mã nhân viên"
        self.table.setItem(row_count, 0, QTableWidgetItem(str(employee_code)))
        self.table.setItem(row_count, 1, QTableWidgetItem(name))
        self.table.setItem(row_count, 2, QTableWidgetItem(role))
        self.table.setItem(row_count, 4, QTableWidgetItem(time_in))
        self.table.setItem(row_count, 5, QTableWidgetItem(time_out))

        late_checkbox = self.create_checkbox_widget(late)
        cp_checkbox = self.create_checkbox_widget(cp)
        kp_checkbox = self.create_checkbox_widget(kp)

        self.table.setCellWidget(row_count, 3, late_checkbox)
        self.table.setCellWidget(row_count, 6, cp_checkbox)
        self.table.setCellWidget(row_count, 7, kp_checkbox)

        # Lưu employee_id vào dữ liệu để sử dụng cho cập nhật
        self.table.item(row_count, 0).setData(QtCore.Qt.ItemDataRole.UserRole, employee_id)

    def create_checkbox_widget(self, checked=False):
        checkbox_widget = QWidget()
        checkbox_layout = QHBoxLayout(checkbox_widget)
        checkbox_layout.setContentsMargins(0, 0, 0, 0)  # Không có margin thừa
        checkbox_layout.setSpacing(0)  # Không có khoảng cách giữa các phần tử
        checkbox = QCheckBox()
        checkbox.setChecked(checked)
        
        checkbox.setStyleSheet("""
            QCheckBox::indicator {
                width: 14px;  /* Kích thước nhỏ gọn */
                height: 14px;
                border-radius: 7px;  /* Hình tròn */
                border: 1px solid #9FEF00;  /* Viền mỏng */
                background-color: #192E44;  /* Màu nền mặc định */
                transition: background-color 0.3s ease, border 0.3s ease;
            }
            QCheckBox::indicator:hover {
                background-color: #2E3A4E;
                border: 1px solid #A4F9C8;
            }
            QCheckBox::indicator:checked {
                background-color: #68D477;
                border: 1px solid #68D477;
                image: url("src/fe/Image_and_icon/icons8-checkmark-20.png");
            }
            QCheckBox::indicator:unchecked {
                background-color: #192E44;
            }
        """)
        
        checkbox_layout.addWidget(checkbox)
        checkbox_layout.setAlignment(checkbox, QtCore.Qt.AlignmentFlag.AlignCenter)  # Căn giữa hoàn toàn
        checkbox.stateChanged.connect(self.on_checkbox_changed)
        checkbox.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        return checkbox_widget    

    def on_checkbox_changed(self, state):
        sender = self.table.sender()
        if not sender:
            return
        
        row = -1
        column = -1
        for r in range(self.table.rowCount()):
            for c in [3, 6, 7]:  # Cột 3: Muộn, Cột 6: Nghỉ có phép, Cột 7: Nghỉ không phép
                if self.table.cellWidget(r, c) and self.table.cellWidget(r, c).layout().itemAt(0).widget() == sender:
                    row = r
                    column = c
                    break
            if row != -1:
                break

        if row == -1 or column == -1:
            return

        # Nếu checkbox được tích, bỏ tích các checkbox khác trong cùng hàng
        if sender.isChecked():
            for c in [3, 6, 7]:
                if c != column:  # Bỏ qua checkbox vừa được tích
                    other_checkbox_widget = self.table.cellWidget(row, c)
                    if other_checkbox_widget:
                        other_checkbox = other_checkbox_widget.layout().itemAt(0).widget()
                        other_checkbox.setChecked(False)

        # Lấy trạng thái của các checkbox
        is_late = self.table.cellWidget(row, 3).layout().itemAt(0).widget().isChecked()
        is_permission_absent = self.table.cellWidget(row, 6).layout().itemAt(0).widget().isChecked()
        is_absent = self.table.cellWidget(row, 7).layout().itemAt(0).widget().isChecked()

        # Lấy employee_id và date
        employee_id = self.table.item(row, 0).data(QtCore.Qt.ItemDataRole.UserRole)
        date = self.date_edit.date().toString("yyyy-MM-dd")
        print(f"Cập nhật trạng thái: employee_id={employee_id}, date={date}, is_late={is_late}, is_permission_absent={is_permission_absent}, is_absent={is_absent}")

        self.update_attendance(employee_id, date, is_late, is_permission_absent, is_absent)

    def update_attendance(self, employee_id, date, is_late, is_permission_absent, is_absent):
        # Đảm bảo date là ngày được chọn từ QDateEdit
        date = self.date_edit.date().toString("yyyy-MM-dd")
        print(f"Ngày được truyền vào API update-attendance: {date}")

        settings = QSettings("MyApp", "LoginApp")
        token = settings.value("access_token", None)
        if not token:
            print("Không có token, không thể cập nhật điểm danh")
            QtWidgets.QMessageBox.warning(self.centralwidget, "Lỗi", "Không có token, vui lòng đăng nhập lại.")
            return

        headers = {"Authorization": f"Bearer {token}"}
        url = f"http://127.0.0.1:8000/attendance/update-attendance/{employee_id}"
        data = {
            "date": date,
            "is_late": is_late,
            "is_permission_absent": is_permission_absent,
            "is_absent": is_absent
        }

        print(f"Gọi API update-attendance: {url} với data: {data}")
        try:
            response = requests.put(url, json=data, headers=headers)
            response.raise_for_status()
            print(f"Cập nhật điểm danh thành công cho employee_id {employee_id}")
            # Tải lại dữ liệu với cùng ngày đã sử dụng để cập nhật
            self.load_attendance_data(date)
        except requests.RequestException as e:
            print(f"Lỗi khi cập nhật điểm danh: {str(e)}")
            QtWidgets.QMessageBox.warning(self.centralwidget, "Lỗi", f"Lỗi khi cập nhật điểm danh: {str(e)}")

class CheckingUI(QtWidgets.QMainWindow):
    switch_to_day_signal = pyqtSignal()
    switch_to_month_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.ui = Ui_checkingUI()
        self.ui.setupUi(self)
        
        self.ui.btn_day_attendance.clicked.connect(self.load_data_and_switch_to_day)
        self.ui.btn_month_attendance.clicked.connect(self.switch_to_month_signal.emit)
        
        self.ui.date_edit.dateChanged.connect(self.on_date_changed)

        # Tải dữ liệu điểm danh của ngày hôm nay ngay khi khởi tạo giao diện
        if not self.ui.load_attendance_data():
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Không thể tải dữ liệu điểm danh. Vui lòng kiểm tra kết nối hoặc đăng nhập lại.")

    def load_data_and_switch_to_day(self):
        if self.ui.load_attendance_data():
            self.switch_to_day_signal.emit()
        else:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng đăng nhập để tải dữ liệu điểm danh.")

    def on_date_changed(self, date):
        self.ui.load_attendance_data(date.toString("yyyy-MM-dd"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    checkingUI = CheckingUI()
    checkingUI.show()
    sys.exit(app.exec())