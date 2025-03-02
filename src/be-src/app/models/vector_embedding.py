from sqlalchemy import Column, Integer, LargeBinary, ForeignKey
from app.core.database import Base
from sqlalchemy.orm import relationship

class EmployeeEmbedding(Base):
    __tablename__ = "employee_embeddings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    embedding = Column(LargeBinary, nullable=False)  
    user = relationship("User", back_populates="embeddings")
