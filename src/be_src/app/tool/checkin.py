import os
import pickle
import cv2
import numpy as np
import torch
from datetime import datetime, date, time, timedelta
from facenet_pytorch import MTCNN, InceptionResnetV1
from torchvision import transforms
import sys
import json
import time as time_module

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from app.models.attendance import Attendance
from app.models.employees import Employee
from app.core.database import SessionLocal

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EMBEDDING_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "..", "..", "data", "embedding"))
print(EMBEDDING_DIR)

# Load embedding đã lưu
known_embeddings = {}
for filename in os.listdir(EMBEDDING_DIR):
    if filename.endswith(".pkl"):
        employee_code = os.path.splitext(filename)[0]
        file_path = os.path.join(EMBEDDING_DIR, filename)
        with open(file_path, "rb") as f:
            embedding = pickle.load(f)
        known_embeddings[employee_code] = embedding

# Chọn device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Khởi tạo MTCNN và InceptionResnetV1
mtcnn = MTCNN(keep_all=True, device=device)
resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)

# Hàm chuyển đổi hình ảnh khuôn mặt thành tensor
transform = transforms.Compose([transforms.ToTensor()])

# Mở camera
cap = cv2.VideoCapture(0)

# Ngưỡng khoảng cách
THRESHOLD = 0.9

# Thời gian thông báo cuối cùng
last_notification_time = 0
NOTIFICATION_INTERVAL = 5  # Khoảng cách 5 giây giữa các thông báo

# Thời gian quy định từ attendance_service.py
CHECK_IN_TIME = datetime.strptime("08:00:00", "%H:%M:%S").time()
LATE_THRESHOLD = timedelta(minutes=15)  # 15 phút
ABSENT_THRESHOLD = timedelta(hours=1)   # 1 giờ

while True:
    ret, frame = cap.read()
    if not ret:
        break

    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    boxes, _ = mtcnn.detect(img_rgb)
    
    if boxes is not None:
        for box in boxes:
            x1, y1, x2, y2 = [int(b) for b in box]
            face_img = img_rgb[y1:y2, x1:x2]
            try:
                face_img = cv2.resize(face_img, (160, 160))
            except Exception as e:
                continue
            
            face_tensor = transform(face_img).unsqueeze(0).to(device)
            with torch.no_grad():
                embedding = resnet(face_tensor)
            
            best_match = None
            best_distance = float("inf")
            for emp_code, known_emb in known_embeddings.items():
                if isinstance(known_emb, np.ndarray):
                    known_emb = torch.tensor(known_emb).to(device)
                distance = (embedding - known_emb).norm().item()
                if distance < best_distance:
                    best_distance = distance
                    best_match = emp_code
            
            if best_distance < THRESHOLD:
                label = f"Matched: {best_match} (dist: {best_distance:.2f})"
                
                # Kiểm tra thời gian kể từ thông báo cuối cùng
                current_time = time_module.time()
                if current_time - last_notification_time >= NOTIFICATION_INTERVAL:
                    session = SessionLocal()
                    try:
                        today = date.today()
                        existing_attendance = session.query(Attendance).filter(
                            Attendance.employee_code == best_match,
                            Attendance.date == today
                        ).first()
                        
                        temp_file = os.path.join(BASE_DIR, "..", "..", "..", "..", "checkin_notification.json")
                        employee = session.query(Employee).filter(Employee.employee_code == best_match).first()
                        full_name = employee.full_name if employee else "Unknown"
                        
                        if existing_attendance:
                            print(f"Nhân viên {best_match} đã điểm danh hôm nay, bỏ qua.")
                            notification_data = {
                                "full_name": full_name,
                                "check_in_time": existing_attendance.check_in_time.strftime("%H:%M:%S %d/%m/%Y"),
                                "status": "already_checked_in"
                            }
                            with open(temp_file, "w", encoding="utf-8") as f:
                                json.dump(notification_data, f, ensure_ascii=False)
                            print(f"Đã ghi thông báo check-in vào {temp_file}")
                        else:
                            check_in_time = datetime.now()
                            # Tính toán is_late và is_absent dựa trên CHECK_IN_TIME
                            check_in_datetime = datetime.combine(today, check_in_time.time())
                            check_in_threshold = datetime.combine(today, CHECK_IN_TIME)
                            late_threshold_time = check_in_threshold + LATE_THRESHOLD
                            absent_threshold_time = check_in_threshold + ABSENT_THRESHOLD

                            # Logic mới: 
                            # - Quá 15 phút nhưng dưới 1 tiếng: chỉ đánh dấu is_late
                            # - Quá 1 tiếng: chỉ đánh dấu is_absent
                            if check_in_datetime > absent_threshold_time:
                                is_late = False
                                is_absent = True
                            elif check_in_datetime > late_threshold_time:
                                is_late = True
                                is_absent = False
                            else:
                                is_late = False
                                is_absent = False

                            attendance = Attendance(
                                employee_code=best_match,
                                check_in_time=check_in_time,
                                date=today,
                                is_late=is_late,
                                is_absent=is_absent,
                                is_permission_absent=False  # Mặc định không xin phép nghỉ
                            )
                            session.add(attendance)
                            session.commit()
                            session.refresh(attendance)
                            print(f"Đã lưu điểm danh cho {best_match} - Muộn: {is_late}, Vắng: {is_absent}")

                            # Chuẩn bị thông báo với trạng thái phù hợp
                            if is_absent:
                                status_message = "vắng mặt"
                            elif is_late:
                                status_message = "đi muộn"
                            else:
                                status_message = "đúng giờ"

                            notification_data = {
                                "full_name": full_name,
                                "check_in_time": check_in_time.strftime("%H:%M:%S %d/%m/%Y"),
                                "status": "success",
                                "message": f"Nhân viên {full_name} đã check-in {status_message}"
                            }
                            with open(temp_file, "w", encoding="utf-8") as f:
                                json.dump(notification_data, f, ensure_ascii=False)
                            print(f"Đã ghi thông báo check-in vào {temp_file}")
                        
                        # Cập nhật thời gian thông báo cuối cùng
                        last_notification_time = current_time
                    except Exception as e:
                        print("Lỗi khi lưu điểm danh hoặc ghi thông báo:", e)
                        session.rollback()
                    finally:
                        session.close()
            else:
                label = f"Unknown (dist: {best_distance:.2f})"
            
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 2)

    cv2.imshow("Check-in", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()