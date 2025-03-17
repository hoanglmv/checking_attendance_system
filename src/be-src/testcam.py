import cv2
import torch
import numpy as np
import os
import pickle
from facenet_pytorch import InceptionResnetV1, MTCNN
from scipy.spatial.distance import cosine

# Khởi tạo model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
mtcnn = MTCNN(image_size=160, margin=10, keep_all=False, device=device)
facenet = InceptionResnetV1(pretrained="vggface2").eval().to(device)

# Load embeddings đã lưu
def load_embeddings(embedding_dir="data/embedding"):
    embeddings = {}
    for file in os.listdir(embedding_dir):
        if file.endswith(".pkl"):  
            file_path = os.path.join(embedding_dir, file)
            with open(file_path, "rb") as f:
                embeddings[file] = pickle.load(f)  # Lưu theo tên file
    return embeddings

# Hàm lấy embedding từ ảnh khuôn mặt
def get_embedding(face):
    face = face.unsqueeze(0).to(device)
    with torch.no_grad():
        embedding = facenet(face)
    return embedding.cpu().numpy().flatten()

# So sánh embedding với database
def recognize_face(face, embeddings, threshold=0.5):
    input_embedding = get_embedding(face)
    best_match = "Unknown"
    best_distance = float("inf")

    for file_name, saved_embedding in embeddings.items():
        distance = cosine(input_embedding, saved_embedding)
        if distance < best_distance and distance < threshold:
            best_match = file_name  # Lưu tên file của vector giống nhất
            best_distance = distance

    return best_match

# Chạy nhận diện trên webcam
def run_webcam():
    embeddings = load_embeddings()
    cap = cv2.VideoCapture(0)  # Mở webcam

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face = mtcnn(img_rgb)

        if face is not None:
            match_file = recognize_face(face, embeddings)
            cv2.putText(frame, match_file, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Face Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):  
            break

    cap.release()
    cv2.destroyAllWindows()

# Chạy chương trình
if __name__ == "__main__":
    run_webcam()
