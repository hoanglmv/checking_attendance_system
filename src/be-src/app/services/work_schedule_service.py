from sqlalchemy.orm import Session
from app.models.work_schedule_model import WorkSchedule
from app.schemas.work_schedule_schema import WorkScheduleCreate

def create_work_schedule(db: Session, schedule: WorkScheduleCreate):
    db_schedule = WorkSchedule(
        shift_name=schedule.shift_name,
        start_time=schedule.start_time,
        end_time=schedule.end_time
    )
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule
