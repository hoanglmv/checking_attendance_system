from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.vector_embedding import EmployeeEmbedding

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    employee_code = Column(String(255), unique=True, index=True, nullable=False)  
    full_name = Column(String(255), nullable=False)
    position = Column(String(255), nullable=False)  
    department = Column(String(255), nullable=False)  
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(255), nullable=True)
    face_embedding = Column(LargeBinary, nullable=True)  

    attendances = relationship("Attendance", back_populates="employee")
    embedding = relationship("EmployeeEmbedding", back_populates="employee", uselist=False)


    
