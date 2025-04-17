import os
import pickle
import cv2
import numpy as np
import torch
from datetime import datetime
from facenet_pytorch import MTCNN, InceptionResnetV1
from torchvision import transforms
import sys

# Thêm dòng này để hỗ trợ hiển thị tiếng Việt
sys.stdout.reconfigure(encoding='utf-8')

# Thêm đường dẫn chứa thư mục 'app'
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

# Import model Attendance và session database (điều chỉnh lại đường dẫn import theo dự án của bạn)
from app.models.attendance import Attendance
from app.core.database import SessionLocal

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EMBEDDING_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "..", "..", "data", "embedding"))
print(EMBEDDING_DIR)

# Load embedding đã lưu (giả sử mỗi file .pkl chứa 1 vector embedding dạng numpy array)
known_embeddings = {}
for filename in os.listdir(EMBEDDING_DIR):
    if filename.endswith(".pkl"):
        employee_code = os.path.splitext(filename)[0]
        file_path = os.path.join(EMBEDDING_DIR, filename)
        with open(file_path, "rb") as f:
            embedding = pickle.load(f)
        known_embeddings[employee_code] = embedding

# Chọn device (GPU nếu có)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Khởi tạo MTCNN để phát hiện khuôn mặt
mtcnn = MTCNN(keep_all=True, device=device)

# Khởi tạo mô hình InceptionResnetV1 với trọng số pretrained (ví dụ trên vggface2)
resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)

# Hàm chuyển đổi hình ảnh khuôn mặt thành tensor
transform = transforms.Compose([
    transforms.ToTensor()
])

# Mở camera
cap = cv2.VideoCapture(1)

# Ngưỡng khoảng cách để xác định trùng khớp (có thể cần điều chỉnh)
THRESHOLD = 0.9

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Chuyển đổi ảnh từ BGR (OpenCV) sang RGB
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Phát hiện các khuôn mặt trong hình, boxes có dạng mảng [[x1, y1, x2, y2], ...]
    boxes, _ = mtcnn.detect(img_rgb)
    
    if boxes is not None:
        for box in boxes:
            # Làm tròn tọa độ bounding box
            x1, y1, x2, y2 = [int(b) for b in box]
            
            # Cắt vùng khuôn mặt và resize về kích thước 160x160
            face_img = img_rgb[y1:y2, x1:x2]
            try:
                face_img = cv2.resize(face_img, (160, 160))
            except Exception as e:
                continue  # Bỏ qua nếu không resize được
            
            # Chuyển hình ảnh sang tensor và thêm batch dimension
            face_tensor = transform(face_img).unsqueeze(0).to(device)
            
            # Tính vector embedding cho khuôn mặt
            with torch.no_grad():
                embedding = resnet(face_tensor)
            
            # So sánh embedding với các embedding đã lưu
            best_match = None
            best_distance = float("inf")
            for emp_code, known_emb in known_embeddings.items():
                # Nếu embedding lưu ở dạng numpy array, chuyển về tensor
                if isinstance(known_emb, np.ndarray):
                    known_emb = torch.tensor(known_emb).to(device)
                distance = (embedding - known_emb).norm().item()
                if distance < best_distance:
                    best_distance = distance
                    best_match = emp_code
            
            # Nếu khoảng cách nhỏ hơn ngưỡng thì xác định là trùng khớp
            if best_distance < THRESHOLD:
                label = f"Matched: {best_match} (dist: {best_distance:.2f})"
                
                try:
                    # Sử dụng context manager để đảm bảo phiên làm việc được đóng sau khi dùng
                    with SessionLocal() as session:
                        checkout_date = datetime.now().date()
                        # Tìm bản ghi điểm danh của nhân viên trong ngày
                        attendance = session.query(Attendance).filter(
                            Attendance.employee_code == best_match,
                            Attendance.date == checkout_date
                        ).first()
                        
                        if attendance:
                            if attendance.check_out_time is None:
                                attendance.check_out_time = datetime.now()
                                session.commit()
                                session.refresh(attendance)
                                print(f"Đã cập nhật checkout cho {best_match}")
                            else:
                                print(f"Nhân viên {best_match} đã checkout rồi hôm nay.")
                        else:
                            print(f"Không tìm thấy bản ghi check-in cho {best_match} ngày hôm nay")
                except Exception as e:
                    print("Lỗi khi cập nhật checkout:", e)
            else:
                label = f"Unknown (dist: {best_distance:.2f})"
            
            # Vẽ bounding box và label lên ảnh
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 2)

    # Hiển thị video
    cv2.imshow("Checkout", frame)
    
    # Thoát bằng phím 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
