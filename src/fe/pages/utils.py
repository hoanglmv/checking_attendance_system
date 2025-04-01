# E:\AttendanceCheckingApp\checking_attendance_system\src\fe\pages\utils.py
from pathlib import Path
import cv2
import numpy as np
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
import requests
import os
from PyQt6 import QtCore
from email_validator import validate_email, EmailNotValidError
import torch
import pickle
from torchvision import transforms

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

def process_and_save_face(frame, mtcnn, facenet, employee_id):
    """
    Phát hiện khuôn mặt trong frame, crop khuôn mặt, tính embedding và lưu vào file .pkl
    :param frame: Ảnh gốc từ camera (BGR)
    :param mtcnn: Instance của MTCNN
    :param facenet: Instance của FaceNet (InceptionResnetV1)
    :param employee_id: ID nhân viên dùng làm tên file
    """
    # Chuyển frame sang RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Phát hiện khuôn mặt
    boxes, probs = mtcnn.detect(frame_rgb)
    print("Boxes:", boxes)
    print("Probs:", probs)
    
    if boxes is None or len(boxes) == 0:
        print("Không phát hiện được khuôn mặt để crop.")
        return
    
    # Chọn bounding box đầu tiên (hoặc thay bằng bbox có xác suất cao nhất nếu cần)
    box = boxes[0]
    x1, y1, x2, y2 = map(int, box)
    face_img = frame_rgb[y1:y2, x1:x2]
    print("Kích thước face_img:", face_img.shape)
    
    # Chuyển đổi ảnh crop thành tensor, resize và normalize theo yêu cầu của mô hình FaceNet
    transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((160, 160)),
        transforms.ToTensor(),
        transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
    ])
    
    try:
        face_tensor = transform(face_img).unsqueeze(0)
        face_tensor = face_tensor.to(next(facenet.parameters()).device)
    except Exception as e:
        print("Lỗi khi chuyển đổi ảnh:", e)
        return
    
    # Tính embedding của khuôn mặt
    try:
        with torch.no_grad():
            embedding = facenet(face_tensor).squeeze().cpu().numpy()
        print("Embedding shape:", embedding.shape)
    except Exception as e:
        print("Lỗi khi tính embedding:", e)
        return
    
    # Lưu embedding vào file .pkl
    project_root = Path(__file__).resolve().parent.parent.parent.parent  # Từ src lên checking_attendance_system
    save_dir = project_root / "data" / "embedding"  # Đi vào data/embedding

    try:
        save_dir.mkdir(parents=True, exist_ok=True)  # Tạo thư mục nếu chưa tồn tại
    except Exception as e:
        print("Lỗi khi tạo thư mục lưu file:", e)
        return

    save_path = save_dir / f"{employee_id}.pkl"  # Tạo đường dẫn tới file .pkl
    try:
        with open(save_path, 'wb') as f:
            pickle.dump(embedding, f)
        print(f"Embedding của nhân viên {employee_id} đã được lưu tại {save_path}")
    except Exception as e:
        print("Lỗi khi lưu file .pkl:", e)


def add_new_employee(ui, mtcnn, facenet):
    """Gửi thông tin nhân viên và ảnh lên API, đồng thời crop khuôn mặt và lưu embedding vào file .pkl"""
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
            if not os.path.exists(ui.add_employee_ui.selected_image_path):
                QMessageBox.warning(None, "Lỗi", "File ảnh không tồn tại! Vui lòng chọn lại ảnh.")
                return
            file_obj = open(ui.add_employee_ui.selected_image_path, 'rb')
            files['file'] = ('avatar.jpg', file_obj, 'image/jpeg')
        except Exception as e:
            QMessageBox.warning(None, "Lỗi", f"Không thể đọc file ảnh: {str(e)}")
            return

    try:
        print(f"Đang gửi dữ liệu lên API: {employee_data}")
        if files:
            print(f"Đang gửi file: {ui.add_employee_ui.selected_image_path}")
        response = requests.post(api_url, data=employee_data, files=files, headers=headers)
        response.raise_for_status()
        if response.status_code == 201:
            QMessageBox.information(None, "Thành công", "Đã thêm nhân viên mới!")
            # Lấy employee_code từ phản hồi JSON
            data = response.json()
            employee_code = data.get("employee_code")
            if not employee_code:
                QMessageBox.warning(None, "Lỗi", "Server không trả về employee_code!")
                return
            ui.load_employees_from_api()  # Tải lại danh sách nhân viên

            # Sau khi lưu thành công, crop khuôn mặt từ camera và lưu embedding với tên file là employee_code.pkl
            if employee_code and ui.add_employee_ui.cap is not None and ui.add_employee_ui.cap.isOpened():
                ret, frame = ui.add_employee_ui.cap.read()
                if ret:
                    process_and_save_face(frame, mtcnn, facenet, employee_code)
                else:
                    print("Không đọc được khung hình từ camera để crop khuôn mặt.")
            else:
                print("Không có employee_code hoặc camera chưa khởi tạo.")

            # Reset giao diện: xóa các trường nhập liệu và reset ảnh hiển thị
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
        if file_obj:
            try:
                file_obj.close()
            except Exception as e:
                print(f"Không thể đóng file ảnh: {str(e)}")

