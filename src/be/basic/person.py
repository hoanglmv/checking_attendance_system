import numpy as np
from be.basic.face_embedding import FaceEmbedding  # Import class FaceEmbedding

class Personal:
    def __init__(self, per_id: str, name: str, position: str, gmail: str, phone_number: str, 
                 face_embedding=None, profile_image: str = None):
        """
        Constructor
        """
        self._per_id = per_id
        self._name = name
        self._position = position
        self._gmail = gmail
        self._phone_number = phone_number
        self._face_embedding = np.array(face_embedding) if face_embedding is not None else np.array([])
        self._profile_image = profile_image
        self._face_embedder = FaceEmbedding()  # Khởi tạo bộ trích xuất embedding

        # Nếu có ảnh, tự động trích xuất embedding
        if profile_image:
            self.update_face_embedding(profile_image)

    # Getter & Setter for per_id
    @property
    def per_id(self):
        return self._per_id

    @per_id.setter
    def per_id(self, value):
        self._per_id = value

    # Getter & Setter for name
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    # Getter & Setter for position
    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    # Getter & Setter for gmail
    @property
    def gmail(self):
        return self._gmail

    @gmail.setter
    def gmail(self, value):
        self._gmail = value

    # Getter & Setter for phone_number
    @property
    def phone_number(self):
        return self._phone_number

    @phone_number.setter
    def phone_number(self, value):
        self._phone_number = value

    # Getter for face_embedding
    @property
    def face_embedding(self):
        return self._face_embedding

    # Getter & Setter for profile_image
    @property
    def profile_image(self):
        return self._profile_image

    @profile_image.setter
    def profile_image(self, value):
        self._profile_image = value
        self.update_face_embedding(value)  # Tự động cập nhật embedding khi đặt ảnh mới

    def update_face_embedding(self, image_path):
        """Cập nhật embedding khuôn mặt khi có ảnh mới"""
        embedding = self._face_embedder.get_embedding(image_path)
        if embedding is not None:
            self._face_embedding = embedding
        else:
            print(f"Không tìm thấy khuôn mặt trong ảnh: {image_path}")

    def get_info(self):
        """Trả về thông tin nhân viên dưới dạng dict"""
        return {
            "ID": self._per_id,
            "Name": self._name,
            "Position": self._position,
            "Email": self._gmail,
            "Phone": self._phone_number,
            "Profile Image": self._profile_image if self._profile_image else "Chưa có ảnh"
        }

    def __str__(self):
        return f"Employee(ID: {self._per_id}, Name: {self._name}, Position: {self._position}, " \
               f"Email: {self._gmail}, Phone: {self._phone_number}, Image: {self._profile_image})"
