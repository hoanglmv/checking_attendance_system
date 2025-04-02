import requests
from PyQt6 import QtCore, QtWidgets, QtGui
from datetime import datetime, date

class AttendanceCalendar(QtWidgets.QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            background-color: #192E44;
            border-radius: 8px;
        """)
        
        # Dictionary để lưu trữ màu của từng ngày
        self.date_colors = {}

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout.setSpacing(5)

        # Content header
        self.content_header = QtWidgets.QGroupBox(self)
        self.content_header.setStyleSheet("""
            border: none;
            background-color: #223850;
            border-radius: 5px;
            padding: 5px;
        """)
        self.contentHeaderLayout = QtWidgets.QHBoxLayout(self.content_header)
        self.contentHeaderLayout.setContentsMargins(5, 0, 5, 0)
        self.contentHeaderLayout.setSpacing(10)

        self.pushButton = QtWidgets.QPushButton("Chọn nhân viên", self.content_header)
        self.pushButton.setStyleSheet("""
            QPushButton {
                border: none;
                color: white;
                font: 10pt 'Times New Roman';
                background-color: #34495E;
                border-radius: 5px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #4A6076;
                color: #FFFFFF;
            }
            QPushButton:pressed {
                background-color: #2C3E50;
            }
        """)
        self.pushButton.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, 
                                                           QtWidgets.QSizePolicy.Policy.Fixed))
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.contentHeaderLayout.addWidget(self.pushButton)
        self.contentHeaderLayout.addStretch()

        for color, text in [("#FF0000", "Không phép"), ("#0000FF", "Có phép"), 
                          ("#FFFF00", "Muộn"), ("#00FF00", "Đúng giờ")]:
            tooltip = self.tooltip(self.content_header, color, text)
            self.contentHeaderLayout.addWidget(tooltip)
            self.contentHeaderLayout.addSpacing(5)

        self.verticalLayout.addWidget(self.content_header)

        # Calendar
        self.calendar = QtWidgets.QCalendarWidget(self)
        self.calendar.setGridVisible(True)
        self.calendar.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
        self.calendar.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, 
                                                        QtWidgets.QSizePolicy.Policy.Expanding))
        self.calendar.setStyleSheet("""
            QCalendarWidget QWidget {
                alternate-background-color: #2C3E50;
                color: white;
                border-radius: 5px;
            }
            QCalendarWidget QToolButton {
                color: white;
                font-size: 12px;
                font-weight: bold;
                background-color: #34495E;
                padding: 6px;
                border: none;
                border-radius: 5px;
                margin: 2px;
            }
            QCalendarWidget QToolButton:hover {
                background-color: #4A6076;
            }
            QCalendarWidget QToolButton:pressed {
                background-color: #2C3E50;
            }
            QCalendarWidget QHeaderView {
                background-color: #34495E;
                color: white;
                font-weight: bold;
                font-size: 12px;
            }
            QCalendarWidget QTableView {
                selection-background-color: transparent;
                color: white;
                font-size: 11px;
                gridline-color: #34495E;
                background-color: #223850;
                border-radius: 5px;
                padding: 3px;
            }
            QCalendarWidget QTableView::item:selected {
                background-color: transparent;  /* Giữ nguyên màu nền gốc */
                border: 2px solid #9FEF00;     /* Chỉ thêm viền để biểu thị chọn */
                color: white;
            }
            QCalendarWidget QTableView:disabled {
                color: #555555;
            }
        """)
        self.calendar.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.calendar.currentPageChanged.connect(self.on_calendar_month_changed)
        self.calendar.clicked.connect(self.on_date_clicked)
        self.calendar.selectionChanged.connect(self.on_selection_changed)

        scroll_area = QtWidgets.QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.calendar)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #34495E;
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #4A6076;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar:horizontal {
                border: none;
                background: #34495E;
                height: 8px;
                margin: 0px;
            }
            QScrollBar::handle:horizontal {
                background: #4A6076;
                border-radius: 4px;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
            }
        """)
        self.verticalLayout.addWidget(scroll_area)

        self.start_date = None
        self.current_date = QtCore.QDate.currentDate()

    def tooltip(self, pr, color, text):
        container = QtWidgets.QWidget(parent=pr)
        container.setStyleSheet("background: transparent;")
        layout = QtWidgets.QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(3)

        icon_button = QtWidgets.QPushButton(container)
        icon_button.setFixedSize(QtCore.QSize(20, 20))
        icon_button.setStyleSheet(f"""
            QPushButton {{
                border: none;
                background-color: {color};
                border-radius: 10px;
                padding: 2px;
            }}
            QPushButton:hover {{
                opacity: 0.8;
                transform: scale(1.1);
            }}
        """)
        icon_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

        text_button = QtWidgets.QPushButton(text, container)
        text_button.setStyleSheet("""
            QPushButton {
                border: none;
                color: white;
                font: 9pt 'Times New Roman';
                padding: 4px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
                color: #FFFFFF;
            }
        """)
        text_button.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, 
                                                       QtWidgets.QSizePolicy.Policy.Fixed))
        text_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

        layout.addWidget(icon_button)
        layout.addWidget(text_button)
        return container

    def on_employee_clicked(self, item):
        print("Bắt đầu on_employee_clicked")
        try:
            emp = item.data(QtCore.Qt.ItemDataRole.UserRole)
            if not emp:
                print("Không có dữ liệu nhân viên")
                QtWidgets.QMessageBox.warning(None, "Lỗi", "Không tìm thấy thông tin nhân viên!")
                return
            print(f"Nhân viên được chọn: {emp}")
            self.current_employee = emp
            self.pushButton.setText(f"{emp['id']} - {emp['name']} - {emp['office']}")
            
            start_date_str = emp.get('start_date')
            if start_date_str:
                self.start_date = QtCore.QDate.fromString(start_date_str, "yyyy-MM-dd")
                if not self.start_date.isValid():
                    print(f"start_date không hợp lệ: {start_date_str}")
                    self.start_date = None
            else:
                print("Không có start_date trong dữ liệu nhân viên")
                self.start_date = None

            year = self.calendar.yearShown()
            month = self.calendar.monthShown()
            print(f"Tải điểm danh cho employee_id: {emp['employee_id']}, năm: {year}, tháng: {month}")
            
            self.load_attendance(emp["employee_id"], year, month)
            self.update_calendar_interaction()
        except Exception as e:
            print(f"Lỗi trong on_employee_clicked: {str(e)}")
            QtWidgets.QMessageBox.critical(None, "Lỗi", f"Có lỗi xảy ra khi chọn nhân viên: {str(e)}")
        print("Kết thúc on_employee_clicked")

    def on_calendar_month_changed(self, year, month):
        if hasattr(self, 'current_employee') and self.current_employee:
            self.load_attendance(self.current_employee["employee_id"], year, month)
            self.update_calendar_interaction()

    def on_date_clicked(self, date):
        if not self.is_date_interactive(date):
            self.calendar.setSelectedDate(self.calendar.selectedDate())
            return
        # Khôi phục màu nền ngay sau khi click
        self.restore_date_color(date)

    def on_selection_changed(self):
        # Khi ngày được chọn thay đổi, khôi phục màu nền của ngày được chọn
        selected_date = self.calendar.selectedDate()
        self.restore_date_color(selected_date)

    def restore_date_color(self, date):
        # Khôi phục màu nền của ngày nếu có
        date_key = date.toString("yyyy-MM-dd")
        fmt = QtGui.QTextCharFormat()
        
        # Áp dụng màu nền nếu ngày có trong date_colors
        if date_key in self.date_colors:
            color = self.date_colors[date_key]
            fmt.setBackground(QtGui.QBrush(QtGui.QColor(color)))
        
        fmt.setToolTip(f"Ngày: {date.toString('dd/MM/yyyy')}")
        if not self.is_date_interactive(date):
            fmt.setForeground(QtGui.QColor("#555555"))
            fmt.setFontItalic(True)
        else:
            fmt.setForeground(QtGui.QColor("white"))
            fmt.setFontItalic(False)
        
        self.calendar.setDateTextFormat(date, fmt)

    def is_date_interactive(self, date):
        if self.start_date and date < self.start_date:
            return False
        if date > self.current_date:
            return False
        if date.dayOfWeek() in (6, 7):
            return False
        return True

    def update_calendar_interaction(self):
        start_date = QtCore.QDate(self.calendar.yearShown(), self.calendar.monthShown(), 1)
        end_date = start_date.addDays(start_date.daysInMonth() - 1)
        current_date = start_date

        while current_date <= end_date:
            fmt = self.calendar.dateTextFormat(current_date)
            if not self.is_date_interactive(current_date):
                fmt.setForeground(QtGui.QColor("#555555"))
                fmt.setFontItalic(True)
            else:
                fmt.setForeground(QtGui.QColor("white"))
                fmt.setFontItalic(False)
            self.calendar.setDateTextFormat(current_date, fmt)
            current_date = current_date.addDays(1)

        if self.start_date:
            self.calendar.setMinimumDate(self.start_date)
        else:
            self.calendar.setMinimumDate(QtCore.QDate(1900, 1, 1))
        self.calendar.setMaximumDate(self.current_date)

    def load_attendance(self, employee_id, year, month):
        print("Bắt đầu load_attendance")
        
        first_day = QtCore.QDate(year, month, 1)
        last_day = first_day.addDays(first_day.daysInMonth() - 1)
        first_displayed_day = first_day.addDays(-(first_day.dayOfWeek() % 7))
        last_displayed_day = last_day.addDays((7 - last_day.dayOfWeek()) % 7)
        
        months_to_load = set()
        current_date = first_displayed_day
        while current_date <= last_displayed_day:
            months_to_load.add((current_date.year(), current_date.month()))
            current_date = current_date.addDays(1)

        all_attendance_data = {}
        settings = QtCore.QSettings("MyApp", "LoginApp")
        access_token = settings.value("access_token")
        if not access_token:
            print("Không có token trong load_attendance")
            QtWidgets.QMessageBox.critical(None, "Lỗi", "Không tìm thấy token. Vui lòng đăng nhập lại!")
            return

        headers = {"Authorization": f"Bearer {access_token}"}
        for y, m in months_to_load:
            url = f"http://127.0.0.1:8000/attendance/{employee_id}/month/{y}/{m}"
            try:
                print(f"Gọi API điểm danh: {url}")
                response = requests.get(url, headers=headers)
                print(f"Phản hồi API: {response.status_code} - {response.text}")
                response.raise_for_status()
                data = response.json()

                if not isinstance(data, dict):
                    print(f"Dữ liệu điểm danh không phải dictionary: {data}")
                    QtWidgets.QMessageBox.warning(None, "Lỗi", "Dữ liệu điểm danh không hợp lệ!")
                    continue

                all_attendance_data[(y, m)] = data
                print(f"Dữ liệu điểm danh cho {y}/{m}: {data}")
            except requests.RequestException as e:
                print(f"Lỗi khi tải dữ liệu cho {y}/{m}: {str(e)}")
                QtWidgets.QMessageBox.critical(None, "Lỗi", f"Không thể tải thông tin điểm danh cho {y}/{m}: {str(e)}")
                continue

        self.clear_calendar()

        current_date = first_displayed_day
        while current_date <= last_displayed_day:
            y, m = current_date.year(), current_date.month()
            date_str = current_date.toString("yyyy-MM-dd")
            data = all_attendance_data.get((y, m), {})

            for date_list, color in [
                (data.get("absent_days", []), "#FF0000"),
                (data.get("permission_absent_days", []), "#0000FF"),
                (data.get("late_days", []), "#FFFF00"),
                (data.get("on_time_days", []), "#00FF00")
            ]:
                if date_str in date_list:
                    print(f"Tô màu {color} cho ngày {date_str}")
                    self.date_colors[date_str] = color  # Lưu màu của ngày
                    self.highlight_date(current_date, color)
                    break

            current_date = current_date.addDays(1)

        print("Kết thúc load_attendance")

    def clear_calendar(self):
        first_day = QtCore.QDate(self.calendar.yearShown(), self.calendar.monthShown(), 1)
        last_day = first_day.addDays(first_day.daysInMonth() - 1)
        first_displayed_day = first_day.addDays(-(first_day.dayOfWeek() % 7))
        last_displayed_day = last_day.addDays((7 - last_day.dayOfWeek()) % 7)

        current_date = first_displayed_day
        while current_date <= last_displayed_day:
            fmt = QtGui.QTextCharFormat()
            self.calendar.setDateTextFormat(current_date, fmt)
            date_str = current_date.toString("yyyy-MM-dd")
            if date_str in self.date_colors:
                del self.date_colors[date_str]  # Xóa màu cũ khi làm mới lịch
            current_date = current_date.addDays(1)

    def highlight_date(self, date, color):
        fmt = QtGui.QTextCharFormat()
        fmt.setBackground(QtGui.QBrush(QtGui.QColor(color)))
        fmt.setToolTip(f"Ngày: {date.toString('dd/MM/yyyy')}")
        if not self.is_date_interactive(date):
            fmt.setForeground(QtGui.QColor("#555555"))
            fmt.setFontItalic(True)
        else:
            fmt.setForeground(QtGui.QColor("white"))
            fmt.setFontItalic(False)
        self.calendar.setDateTextFormat(date, fmt)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    
    main_window = QtWidgets.QMainWindow()
    main_window.setStyleSheet("background-color: #1A2A3A;")
    
    widget = AttendanceCalendar()
    main_window.setCentralWidget(widget)
    
    screen = QtWidgets.QApplication.primaryScreen().geometry()
    window_width = min(800, screen.width() - 100)
    window_height = min(600, screen.height() - 100)
    main_window.resize(window_width, window_height)
    
    main_window.show()
    sys.exit(app.exec())