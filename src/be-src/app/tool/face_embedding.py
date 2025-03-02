import torch
import numpy as np
import pickle
from facenet_pytorch import InceptionResnetV1, MTCNN
from PIL import Image
# Get_Embedding 
class FaceEmbedding:
    def __init__(self, device=None):
        """Khởi tạo mô hình FaceNet pretrain để trích xuất embedding."""
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = InceptionResnetV1(pretrained='vggface2').eval().to(self.device)
        self.mtcnn = MTCNN(image_size=160, margin=10, keep_all=True, device=self.device)

    def get_embedding(self, image_path):
        """Chuyển ảnh khuôn mặt thành vector embedding."""
        image = Image.open(image_path).convert('RGB')
        faces = self.mtcnn(image)

        if faces is None or len(faces) == 0:
            return None
        
        # Chọn khuôn mặt lớn nhất
        if len(faces.shape) == 4:
            sizes = [f.shape[1] * f.shape[2] for f in faces]
            face = faces[torch.argmax(torch.tensor(sizes))]
        else:
            face = faces

        face = face.unsqueeze(0).to(self.device)
        with torch.no_grad():
            embedding = self.model(face)

        return embedding.cpu().numpy().flatten()
