from sqlalchemy import Column, Date, Enum, ForeignKey, Integer, String, Time
from app.core.database import Base
from sqlalchemy.orm import relationship


class WorkSchedule(Base):
    __tablename__ = "work_schedule"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    status = Column(Enum("ACTIVE", "INACTIVE", name="schedule_status"), default="ACTIVE")

    user = relationship("User", back_populates="work_schedules")
