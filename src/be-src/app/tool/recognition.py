import pickle
import numpy as np
from sqlalchemy.orm import Session
from app.models.vector_embedding import EmployeeEmbedding

def save_embedding_to_db(session: Session, employee_id: int, embedding: np.ndarray):
    """Lưu embedding vào cơ sở dữ liệu dưới dạng LargeBinary."""
    serialized_embedding = pickle.dumps(embedding)  # Chuyển NumPy array thành binary
    new_entry = EmployeeEmbedding(
        employee_id=employee_id, 
        embedding=serialized_embedding
    )
    session.add(new_entry)
    session.commit()

def get_embedding_from_db(session: Session, employee_id: int):
    """Truy xuất embedding từ database và chuyển lại thành NumPy array."""
    entry = session.query(EmployeeEmbedding).filter_by(employee_id=employee_id).first()
    if entry:
        return pickle.loads(entry.embedding)  # Chuyển binary về NumPy array
    return None
