import cv2
import torch
import numpy as np
import mysql.connector
from facenet_pytorch import InceptionResnetV1, MTCNN
from scipy.spatial.distance import cosine
from datetime import datetime

# ====== 1. Khởi tạo model và thiết bị ======
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
mtcnn = MTCNN(image_size=160, margin=10, keep_all=False, device=device)
facenet = InceptionResnetV1(pretrained="vggface2").eval().to(device)

# ====== 2. Hàm kết nối MySQL ======
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="hoanglmv",
        database="mlattendance"
    )

# ====== 3. Hàm load embeddings từ MySQL ======
def load_embeddings():
    conn = connect_db()
    cursor = conn.cursor()
    query = "SELECT employee_code, full_name, face_embedding FROM employees"
    cursor.execute(query)
    rows = cursor.fetchall()
    
    embeddings = {}
    for code, name, embedding_blob in rows:
        if embedding_blob:
            embedding = np.frombuffer(embedding_blob, dtype=np.float32)
            embeddings[code] = {
                "full_name": name,
                "embedding": embedding
            }
    
    cursor.close()
    conn.close()
    return embeddings

# ====== 4. Hàm trích xuất embedding từ ảnh khuôn mặt ======
def get_embedding(face):
    face = face.unsqueeze(0).to(device)
    with torch.no_grad():
        embedding = facenet(face)
    return embedding.cpu().numpy().flatten()

# ====== 5. Hàm so sánh embedding với database ======
def recognize_face(face, embeddings, threshold=0.5):
    input_embedding = get_embedding(face)
    best_match = "Unknown"
    best_distance = float("inf")
    best_code = None  # Lưu mã nhân viên
    
    for code, data in embeddings.items():
        saved_embedding = data["embedding"]
        distance = cosine(input_embedding, saved_embedding)
        if distance < best_distance and distance < threshold:
            best_match = data["full_name"]
            best_distance = distance
            best_code = code  # Lưu mã nhân viên tốt nhất
    
    return best_code, best_match

# ====== 6. Hàm kiểm tra và ghi check-in vào database ======
def check_in_employee(employee_code, full_name):
    conn = connect_db()
    cursor = conn.cursor()
    
    today_date = datetime.now().strftime("%Y-%m-%d")
    check_in_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Kiểm tra xem nhân viên đã check-in trong ngày chưa
    query = "SELECT check_in_time FROM attendances WHERE employee_code = %s AND date = %s"
    cursor.execute(query, (employee_code, today_date))
    result = cursor.fetchone()

    if result:
        if result[0] is None:  # Nếu check_in_time là NULL, cập nhật lại
            update_query = """
            UPDATE attendances 
            SET check_in_time = %s 
            WHERE employee_code = %s AND date = %s
            """
            cursor.execute(update_query, (check_in_time, employee_code, today_date))
            conn.commit()
            print(f"[INFO] {full_name} đã cập nhật check-in lúc {check_in_time}.")
        else:
            print(f"[INFO] {full_name} đã check-in hôm nay vào lúc {result[0]}! Không cập nhật lại.")
    else:
        # Nếu chưa check-in, thêm bản ghi mới
        insert_query = """
        INSERT INTO attendances (employee_code, date, check_in_time)
        VALUES (%s, %s, %s)
        """
        cursor.execute(insert_query, (employee_code, today_date, check_in_time))
        conn.commit()
        print(f"[SUCCESS] {full_name} đã check-in lúc {check_in_time}")

    cursor.close()
    conn.close()

# ====== 7. Nhận diện từ Webcam ======
def run_webcam():
    embeddings = load_embeddings()
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face = mtcnn(img_rgb)

        if face is not None:
            employee_code, match_name = recognize_face(face, embeddings)

            if employee_code:
                check_in_employee(employee_code, match_name)

            # Hiển thị kết quả lên màn hình
            cv2.putText(frame, match_name, (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 2)

        cv2.imshow("Face Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

# ====== 8. Chạy chương trình ======
if __name__ == "__main__":
    run_webcam()
