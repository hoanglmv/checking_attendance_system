import cv2
import torch
import numpy as np
import mysql.connector
from facenet_pytorch import InceptionResnetV1, MTCNN
from scipy.spatial.distance import cosine

# ====== 1. Khởi tạo model và thiết bị  ======
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
mtcnn = MTCNN(image_size=160, margin=10, keep_all=False, device=device)
facenet = InceptionResnetV1(pretrained="vggface2").eval().to(device)

# ====== 2. Hàm kết nối MySQL  ======
def connect_db():
    return mysql.connector.connect(
        host="localhost",        # Sửa lại cho đúng nếu cần
        user="root",             # Username
        password="hoanglmv",     # Mật khẩu
        database="mlattendance"  # Tên database
    )

# ====== 3. Hàm load embeddings từ MySQL  ======
def load_embeddings():
    conn = connect_db()
    cursor = conn.cursor()
    
    # Lấy các cột cần thiết: employee_code, full_name, face_embedding
    query = "SELECT employee_code, full_name, face_embedding FROM employees"
    cursor.execute(query)
    rows = cursor.fetchall()
    
    embeddings = {}
    for code, name, embedding_blob in rows:
        if embedding_blob:
            # Vì bạn lưu bằng face_data.tobytes(), nên ta dùng np.frombuffer để chuyển về numpy array.
            # Giả sử dtype của face_data ban đầu là np.float32.
            embedding = np.frombuffer(embedding_blob, dtype=np.float32)
            embeddings[code] = {
                "full_name": name,
                "embedding": embedding
            }
    
    cursor.close()
    conn.close()
    return embeddings

# ====== 4. Hàm trích xuất embedding từ ảnh khuôn mặt  ======
def get_embedding(face):
    face = face.unsqueeze(0).to(device)
    with torch.no_grad():
        embedding = facenet(face)
    return embedding.cpu().numpy().flatten()

# ====== 5. Hàm so sánh embedding với database  ======
def recognize_face(face, embeddings, threshold=0.5):
    input_embedding = get_embedding(face)
    best_match = "Unknown"
    best_distance = float("inf")
    
    # Duyệt qua từng nhân viên trong DB
    for code, data in embeddings.items():
        saved_embedding = data["embedding"]
        distance = cosine(input_embedding, saved_embedding)
        if distance < best_distance and distance < threshold:
            best_match = data["full_name"]  # Hiển thị tên nhân viên
            best_distance = distance
    
    return best_match

# ====== 6. Nhận diện từ Webcam  ======
def run_webcam():
    # 6.1 Tải embeddings từ MySQL
    embeddings = load_embeddings()
    
    # 6.2 Mở webcam
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face = mtcnn(img_rgb)

        if face is not None:
            match_name = recognize_face(face, embeddings)
            # Hiển thị tên nhân viên trên màn hình
            cv2.putText(frame, match_name, (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 2)

        cv2.imshow("Face Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

# ====== 7. Chạy chương trình ======
if __name__ == "__main__":
    run_webcam()
