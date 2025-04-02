import sys
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.database import engine, Base, SessionLocal
from app.routes import auth_routes, attendance_routes, employees_routes
from app.services.auth_service import create_admin_user
from app.services.notification_service import websocket_endpoint
# Import UPLOAD_DIR từ file service
from app.services.employees_service import UPLOAD_DIR
from sqlalchemy_utils import database_exists, create_database  # Thêm import từ sqlalchemy_utils

import sys
sys.stdout.reconfigure(encoding='utf-8')

# Kiểm tra và tạo database nếu chưa tồn tại
if not database_exists(engine.url):
    create_database(engine.url)
    print(f"Database {engine.url.database} đã được tạo.")
else:
    print(f"Database {engine.url.database} đã tồn tại.")

# Tạo bảng trong database
Base.metadata.create_all(bind=engine)

# Khởi tạo ứng dụng FastAPI
app = FastAPI()

# Sử dụng đường dẫn tuyệt đối để đảm bảo tìm đúng thư mục
avt_images_dir = os.path.abspath(UPLOAD_DIR)

# Kiểm tra và tạo thư mục nếu chưa tồn tại
if not os.path.exists(avt_images_dir):
    os.makedirs(avt_images_dir)
    print(f"Đã tạo thư mục: {avt_images_dir}")

# Mount thư mục avt_images với UPLOAD_DIR mới
app.mount("/avt_images", StaticFiles(directory=avt_images_dir), name="avt_images")
print(f"Đã mount thư mục: {avt_images_dir}")

# Khởi tạo ADMIN nếu chưa có
def init_admin():
    db = SessionLocal()
    try:
        create_admin_user(db)
    finally:
        db.close()

init_admin()

app.include_router(auth_routes.router)
app.include_router(attendance_routes.router)
app.include_router(employees_routes.router)

@app.get("/")
def read_root():
    return {"message": "Facial Recognition Attendance System is running!"}

app.add_websocket_route("/ws/admin", websocket_endpoint)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
