from sqlalchemy.orm import Session
from app.models.notification_model import Notification
from app.schemas.notification_schema import NotificationCreate

def create_notification(db: Session, notification: NotificationCreate):
    db_notification = Notification(
        message=notification.message,
        created_at=notification.created_at
    )
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification
