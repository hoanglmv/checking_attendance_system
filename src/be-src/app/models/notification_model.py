from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text
from app.core.database import Base
from sqlalchemy.orm import relationship


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="notifications")


