import os
import pickle
import cv2
import numpy as np
import torch
from datetime import datetime, date, timedelta
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

# Ngưỡng khoảng cách để xác định khuôn mặt phù hợp
THRESHOLD = 0.9

# Thời gian thông báo cuối cùng
last_notification_time = 0
NOTIFICATION_INTERVAL = 5  # 5 giây giữa các thông báo

# Thời gian quy định check-in
CHECK_IN_TIME = datetime.strptime("08:00:00", "%H:%M:%S").time()
LATE_THRESHOLD = timedelta(minutes=15)  # 15 phút
ABSENT_THRESHOLD = timedelta(hours=1)     # 1 giờ

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
                
                current_time = time_module.time()
                if current_time - last_notification_time >= NOTIFICATION_INTERVAL:
                    try:
                        # Lấy thời gian check-in ngay tại thời điểm này
                        check_in_time = datetime.now()
                        # Lấy ngày từ thời gian check-in
                        check_in_date = check_in_time.date()
                        
                        temp_file = os.path.join(BASE_DIR, "..", "..", "..", "..", "checkin_notification.json")
                        
                        # Sử dụng context manager cho phiên làm việc
                        with SessionLocal() as session:
                            employee = session.query(Employee).filter(Employee.employee_code == best_match).first()
                            full_name = employee.full_name if employee else "Unknown"
                            
                            # Kiểm tra xem đã có điểm danh của ngày check-in hay chưa
                            existing_attendance = session.query(Attendance).filter(
                                Attendance.employee_code == best_match,
                                Attendance.date == check_in_date
                            ).first()
                            
                            if existing_attendance:
                                # Nếu đã check-in rồi thì chỉ thông báo
                                print(f"Nhân viên {best_match} đã check-in hôm nay, bỏ qua.")
                                notification_data = {
                                    "full_name": full_name,
                                    "check_in_time": existing_attendance.check_in_time.strftime("%H:%M:%S %d/%m/%Y"),
                                    "status": "already_checked_in",
                                    "message": f"Nhân viên {full_name} đã check-in hôm nay"
                                }
                            else:
                                # Tính toán trạng thái check-in dựa trên thời gian quy định
                                check_in_threshold = datetime.combine(check_in_date, CHECK_IN_TIME)
                                late_threshold_time = check_in_threshold + LATE_THRESHOLD
                                absent_threshold_time = check_in_threshold + ABSENT_THRESHOLD

                                if check_in_time > absent_threshold_time:
                                    is_late = False
                                    is_absent = True
                                elif check_in_time > late_threshold_time:
                                    is_late = True
                                    is_absent = False
                                else:
                                    is_late = False
                                    is_absent = False

                                new_attendance = Attendance(
                                    employee_code=best_match,
                                    check_in_time=check_in_time,
                                    date=check_in_time.date(),  # Lưu ngày lấy từ check_in_time
                                    is_late=is_late,
                                    is_absent=is_absent,
                                    is_permission_absent=False
                                )
                                session.add(new_attendance)
                                session.commit()
                                session.refresh(new_attendance)
                                print(f"Đã lưu điểm danh cho {best_match} - Muộn: {is_late}, Vắng: {is_absent}")

                                if is_absent:
                                    status_message = "vắng mặt"
                                elif is_late:
                                    status_message = "đi muộn"
                                else:
                                    status_message = "đúng giờ"
                                
                                notification_data = {
                                    "full_name": full_name,
                                    "check_in_time": check_in_time.strftime("%H:%M:%S %d/%m/%Y"),
                                    "status": "check_in_success",
                                    "message": f"Nhân viên {full_name} đã check-in {status_message}"
                                }
                        
                        # Ghi file thông báo
                        with open(temp_file, "w", encoding="utf-8") as f:
                            json.dump(notification_data, f, ensure_ascii=False)
                        print(f"Đã ghi thông báo vào {temp_file}")
                        
                        last_notification_time = current_time
                    except Exception as e:
                        print("Lỗi khi lưu điểm danh hoặc ghi thông báo:", e)
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
