from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.services.work_schedule_service import create_work_schedule
from app.schemas.work_schedule_schema import WorkScheduleCreate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create")
def create_schedule(schedule: WorkScheduleCreate, db: Session = Depends(get_db)):
    return create_work_schedule(db, schedule)
