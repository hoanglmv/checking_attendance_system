from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.services.notification_service import create_notification
from app.schemas.notification_schema import NotificationCreate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create")
def create_notification_route(notification: NotificationCreate, db: Session = Depends(get_db)):
    return create_notification(db, notification)
