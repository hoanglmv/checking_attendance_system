import cv2
import numpy as np
import torch
import mysql.connector
from facenet_pytorch import InceptionResnetV1, MTCNN
from PIL import Image
from scipy.spatial.distance import cosine

# Khởi tạo mô hình FaceNet và MTCNN
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
face_encoder = InceptionResnetV1(pretrained="vggface2").eval().to(device)
mtcnn = MTCNN(image_size=160, margin=10, keep_all=False, device=device)

# Kết nối MySQL
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="attendance_system"
    )

# Lấy dữ liệu nhân viên từ database
def get_employee_data():
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, face_embedding FROM employees")
    employees = cursor.fetchall()
    cursor.close()
    conn.close()

    for emp in employees:
        if emp["face_embedding"]:
            emp["face_embedding"] = np.frombuffer(emp["face_embedding"], dtype=np.float32)
    
    return employees

# Tạo embedding từ ảnh
def get_face_embedding(frame):
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    face = mtcnn(image)
    if face is None:
        return None

    face = face.unsqueeze(0).to(device)
    with torch.no_grad():
        embedding = face_encoder(face)
    
    return embedding.cpu().numpy().flatten()

# So sánh embedding để tìm nhân viên phù hợp
def recognize_face(face_embedding, employees, threshold=0.6):
    best_match = None
    min_distance = float("inf")

    for emp in employees:
        if emp["face_embedding"] is None:
            continue

        distance = cosine(face_embedding, emp["face_embedding"])
        if distance < min_distance and distance < threshold:
            min_distance = distance
            best_match = emp

    return best_match

# Lưu chấm công vào database
def mark_attendance(employee_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO attendance (employee_id) VALUES (%s)", (employee_id,))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ Chấm công thành công cho nhân viên ID {employee_id}")

# Mở camera và nhận diện khuôn mặt
def capture_video():
    cap = cv2.VideoCapture(0)
    employees = get_employee_data()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        face_embedding = get_face_embedding(frame)

        if face_embedding is not None:
            matched_employee = recognize_face(face_embedding, employees)
            if matched_employee:
                emp_id, emp_name = matched_employee["id"], matched_employee["name"]
                text = f"ID: {emp_id}, {emp_name}"
                mark_attendance(emp_id)
            else:
                text = "Unknown"

            cv2.putText(frame, text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Face Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_video()
