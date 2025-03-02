from fastapi import FastAPI
from app.core.database import engine, Base, SessionLocal
from app.routes import auth_routes, attendance_routes, work_schedule_routes, notification_routes
from app.services.user_service import create_admin_user

# Tạo bảng trong database
Base.metadata.create_all(bind=engine)

# Khởi tạo ứng dụng FastAPI
app = FastAPI()

# Khởi tạo ADMIN nếu chưa có
def init_admin():
    db = SessionLocal()
    try:
        create_admin_user(db)
    finally:
        db.close()

init_admin()  # Gọi ngay khi app khởi động

# Đăng ký các route
app.include_router(auth_routes.router, prefix="/auth")
app.include_router(attendance_routes.router, prefix="/attendance")
app.include_router(work_schedule_routes.router, prefix="/work-schedule")
app.include_router(notification_routes.router, prefix="/notifications")

@app.get("/")
def read_root():
    return {"message": "Facial Recognition Attendance System is running!"}
