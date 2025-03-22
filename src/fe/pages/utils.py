import cv2
import numpy as np
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
import requests
import os
from PyQt6 import QtCore
from email_validator import validate_email, EmailNotValidError

def update_frame(add_employee_ui, mtcnn):
    """Cập nhật khung hình từ camera và sử dụng MTCNN để phát hiện khuôn mặt"""
    if add_employee_ui.cap is None or not add_employee_ui.cap.isOpened():
        return

    ret, frame = add_employee_ui.cap.read()
    if not ret:
        print("Không thể đọc khung hình từ camera.")
        add_employee_ui.cameraLabel.setText("Không thể đọc camera")
        return

    # Chuyển đổi khung hình sang RGB để sử dụng với MTCNN
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Phát hiện khuôn mặt bằng MTCNN
    boxes, probs = mtcnn.detect(frame_rgb)
    if boxes is not None and probs is not None:
        valid_probs = [p for p in probs if p is not None]
        if valid_probs and max(valid_probs) > 0.9:
            add_employee_ui.instructionLabel.setText("Đã phát hiện khuôn mặt")
            for box in boxes:
                x1, y1, x2, y2 = map(int, box)
                cv2.rectangle(frame_rgb, (x1, y1), (x2, y2), (0, 255, 0), 2)
        else:
            add_employee_ui.instructionLabel.setText("Vui lòng căn chỉnh khuôn mặt của bạn\nvào giữa và nhìn thẳng vào khung hình")
    else:
        add_employee_ui.instructionLabel.setText("Vui lòng căn chỉnh khuôn mặt của bạn\nvào giữa và nhìn thẳng vào khung hình")

    # Chuyển đổi khung hình thành QImage để hiển thị trên QLabel
    height, width, channel = frame_rgb.shape
    bytes_per_line = 3 * width
    q_image = QImage(frame_rgb.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
    pixmap = QPixmap.fromImage(q_image)
    scaled_pixmap = pixmap.scaled(280, 350, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
    add_employee_ui.cameraLabel.setPixmap(scaled_pixmap)
    add_employee_ui.cameraLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

def load_image(add_employee_ui):
    """Chọn và hiển thị ảnh từ máy"""
    file_name, _ = QFileDialog.getOpenFileName(
        None, "Chọn ảnh", "", "Image Files (*.png *.jpg *.jpeg *.bmp)"
    )
    if file_name:
        print(f"Đã chọn ảnh: {file_name}")  # Thêm log để debug
        pixmap = QPixmap(file_name)
        if pixmap.isNull():
            QMessageBox.warning(None, "Lỗi", "Không thể tải ảnh. Vui lòng chọn file ảnh hợp lệ!")
            add_employee_ui.photoLabel2.setText("No Image")
            add_employee_ui.photoLabel2.setAlignment(Qt.AlignmentFlag.AlignCenter)
            add_employee_ui.selected_image_path = None
            return
        scaled_pixmap = pixmap.scaled(140, 168, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        add_employee_ui.photoLabel2.setPixmap(scaled_pixmap)
        add_employee_ui.photoLabel2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        add_employee_ui.selected_image_path = file_name  # Lưu đường dẫn ảnh để gửi lên API
    else:
        add_employee_ui.photoLabel2.setText("No Image")
        add_employee_ui.photoLabel2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        add_employee_ui.selected_image_path = None

def add_new_employee(ui):
    """Gửi thông tin nhân viên và ảnh lên API"""
    settings = QtCore.QSettings("MyApp", "LoginApp")
    access_token = settings.value("access_token")

    if not access_token:
        QMessageBox.critical(None, "Lỗi", "Không tìm thấy access_token. Vui lòng đăng nhập lại!")
        return

    # Lấy thông tin từ các trường nhập liệu
    employee_data = {
        "full_name": ui.add_employee_ui.newLineEdits["Họ tên:"].text().strip(),
        "position": ui.add_employee_ui.newLineEdits["Chức vụ:"].text().strip(),
        "department": ui.add_employee_ui.newLineEdits["Nơi làm việc:"].text().strip(),
        "email": ui.add_employee_ui.newLineEdits["Email:"].text().strip(),
        "phone": ui.add_employee_ui.newLineEdits["Số điện thoại:"].text().strip(),
    }

    # Kiểm tra dữ liệu bắt buộc
    for key, value in employee_data.items():
        if not value:
            QMessageBox.warning(None, "Lỗi", f"Vui lòng điền đầy đủ thông tin: {key}")
            return

    # Kiểm tra định dạng email
    try:
        validate_email(employee_data["email"])
    except EmailNotValidError:
        QMessageBox.warning(None, "Lỗi", "Email không hợp lệ! Vui lòng nhập email đúng định dạng (ví dụ: example@domain.com).")
        return

    # Chuẩn bị dữ liệu gửi lên API
    api_url = "http://127.0.0.1:8000/employees/create"
    headers = {"Authorization": f"Bearer {access_token}"}
    files = {}
    file_obj = None  # Biến để lưu file object

    if hasattr(ui.add_employee_ui, 'selected_image_path') and ui.add_employee_ui.selected_image_path:
        try:
            # Kiểm tra file có tồn tại không
            if not os.path.exists(ui.add_employee_ui.selected_image_path):
                QMessageBox.warning(None, "Lỗi", "File ảnh không tồn tại! Vui lòng chọn lại ảnh.")
                return
            file_obj = open(ui.add_employee_ui.selected_image_path, 'rb')
            files['file'] = ('avatar.jpg', file_obj, 'image/jpeg')
        except Exception as e:
            QMessageBox.warning(None, "Lỗi", f"Không thể đọc file ảnh: {str(e)}")
            return

    try:
        print(f"Đang gửi dữ liệu lên API: {employee_data}")  # Thêm log
        if files:
            print(f"Đang gửi file: {ui.add_employee_ui.selected_image_path}")  # Thêm log
        response = requests.post(api_url, data=employee_data, files=files, headers=headers)
        response.raise_for_status()  # Ném ngoại lệ nếu có lỗi HTTP
        if response.status_code == 201:
            QMessageBox.information(None, "Thành công", "Đã thêm nhân viên mới!")
            ui.load_employees_from_api()  # Tải lại danh sách nhân viên
            # Xóa các trường nhập liệu sau khi lưu thành công
            for line_edit in ui.add_employee_ui.newLineEdits.values():
                line_edit.clear()
            ui.add_employee_ui.photoLabel2.setText("No Image")
            ui.add_employee_ui.photoLabel2.setAlignment(Qt.AlignmentFlag.AlignCenter)
            ui.add_employee_ui.selected_image_path = None
        else:
            QMessageBox.warning(None, "Lỗi", f"Thêm nhân viên thất bại: {response.status_code} - {response.text}")
    except requests.RequestException as e:
        QMessageBox.critical(None, "Lỗi", f"Không thể kết nối đến API: {str(e)}")
    except Exception as e:
        QMessageBox.critical(None, "Lỗi", f"Lỗi không xác định: {str(e)}")
    finally:
        if file_obj:  # Đóng file object, không phải tuple
            try:
                file_obj.close()
            except Exception as e:
                print(f"Không thể đóng file ảnh: {str(e)}")