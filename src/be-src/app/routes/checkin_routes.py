from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.schemas.checkin_schema import AttendanceCreate, AttendanceUpdate, AttendanceResponse
from app.services.checkin_service import (
    create_checkin, update_checkin, get_checkin_by_id, get_all_checkins
)
# Nếu bạn có logic phân quyền (admin, user) thì import ở đây
# from app.utils.dependencies import get_current_admin

router = APIRouter(prefix="/checkin", tags=["Checkin"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=AttendanceResponse)
def create_checkin_endpoint(data: AttendanceCreate, db: Session = Depends(get_db)):
    """Endpoint để tạo một bản ghi attendance (điểm danh)."""
    new_attendance = create_checkin(db, data)
    return new_attendance

@router.get("/", response_model=list[AttendanceResponse])
def get_all_checkins_endpoint(db: Session = Depends(get_db)):
    """Endpoint để lấy tất cả các bản ghi attendance."""
    attendances = get_all_checkins(db)
    return attendances

@router.get("/{attendance_id}", response_model=AttendanceResponse)
def get_checkin_by_id_endpoint(attendance_id: int, db: Session = Depends(get_db)):
    """Endpoint để lấy một bản ghi attendance theo ID."""
    attendance = get_checkin_by_id(db, attendance_id)
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance not found")
    return attendance

@router.put("/{attendance_id}", response_model=AttendanceResponse)
def update_checkin_endpoint(
    attendance_id: int, 
    data: AttendanceUpdate, 
    db: Session = Depends(get_db)
):
    """Endpoint để cập nhật một bản ghi attendance."""
    updated_attendance = update_checkin(db, attendance_id, data)
    if not updated_attendance:
        raise HTTPException(status_code=404, detail="Attendance not found")
    return updated_attendance
