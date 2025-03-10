import os
import torch
import pickle
import numpy as np
from facenet_pytorch import InceptionResnetV1, MTCNN
from PIL import Image

# Định nghĩa đường dẫn lưu trữ
IMAGE_DIR = "data\image"
EMBEDDING_DIR = "data\embedding"
os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(EMBEDDING_DIR, exist_ok=True)

class FaceEmbedding:
    def __init__(self, device=None):
        """Khởi tạo mô hình FaceNet pretrain để trích xuất embedding."""
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = InceptionResnetV1(pretrained='vggface2').eval().to(self.device)
        self.mtcnn = MTCNN(image_size=160, margin=10, keep_all=True, device=self.device)

    def get_embedding(self, image_path, save=True):
        """
        Chuyển ảnh khuôn mặt thành vector embedding và lưu ảnh + embedding.

        Args:
            image_path (str): Đường dẫn ảnh gốc.
            save (bool): Nếu True, lưu ảnh vào folder và embedding dưới dạng .pkl.
        
        Returns:
            np.array: Vector embedding (512 chiều) hoặc None nếu không phát hiện khuôn mặt.
        """
        image = Image.open(image_path).convert('RGB')
        faces = self.mtcnn(image)

        if faces is None or len(faces) == 0:
            print(f"⚠ Không tìm thấy khuôn mặt trong ảnh {image_path}")
            return None
        
        # Nếu có nhiều khuôn mặt, chọn khuôn mặt lớn nhất
        if len(faces.shape) == 4:
            sizes = [f.shape[1] * f.shape[2] for f in faces]
            face = faces[torch.argmax(torch.tensor(sizes))]
        else:
            face = faces

        face = face.unsqueeze(0).to(self.device)

        # Trích xuất embedding
        with torch.no_grad():
            embedding = self.model(face).cpu().numpy().flatten()

        if save:
            filename = os.path.basename(image_path)  # Lấy tên file ảnh gốc
            new_image_path = os.path.join(IMAGE_DIR, filename)  # Lưu ảnh vào folder
            new_embedding_path = os.path.join(EMBEDDING_DIR, f"{os.path.splitext(filename)[0]}.pkl")

            image.save(new_image_path)  # Lưu ảnh
            with open(new_embedding_path, "wb") as f:
                pickle.dump(embedding, f)  # Lưu embedding vào .pkl
            
            print(f"✅ Đã lưu ảnh vào: {new_image_path}")
            print(f"✅ Đã lưu embedding vào: {new_embedding_path}")

        return embedding

image_path = r"data\image\00005.jpg"
face_embedding = FaceEmbedding()
image = face_embedding.get_embedding(image_path)
print("✅ Ảnh đã mở thành công")
