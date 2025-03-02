from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.services.attendance_service import create_attendance, update_checkout
from app.schemas.attendance_schema import AttendanceCreate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/checkin")
def checkin(attendance: AttendanceCreate, db: Session = Depends(get_db)):
    return create_attendance(db, attendance)

@router.put("/checkout/{user_id}")
def checkout(user_id: int, db: Session = Depends(get_db)):
    return update_checkout(db, user_id)
