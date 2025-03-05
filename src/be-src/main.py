from fastapi import FastAPI
from app.models import *
from app.core.database import engine, Base, SessionLocal
from app.routes import auth_routes, attendance_routes, employees_routes
from app.services.auth_service import create_admin_user
from app.services.notification_service import websocket_endpoint
import sys
sys.stdout.reconfigure(encoding='utf-8')

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
app.include_router(employees_routes.router, prefix="/employees")

@app.get("/")
def read_root():
    return {"message": "Facial Recognition Attendance System is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

app.add_websocket_route("/ws/admin", websocket_endpoint)