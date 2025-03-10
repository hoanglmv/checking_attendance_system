import json
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_schema import AdminCreate, AdminUpdate
from app.utils.security import get_password_hash, verify_password, save_otp
from app.services.email_service import send_otp_email
from fastapi import HTTPException
from datetime import datetime
import sys
sys.stdout.reconfigure(encoding='utf-8')

ADMIN_EMAIL = "admin@example.com"  # Email của admin mặc định
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"  # Đổi mật khẩu này sau khi chạy lần đầu

# Tạo tài khoản ADMIN nếu chưa có
def create_admin_user(db: Session):
    admin = db.query(User).first()  # Bỏ kiểm tra role

    if not admin:
        hashed_password = get_password_hash(ADMIN_PASSWORD)
        admin_user = User(
            full_name="Administrator",  # Đặt tên mặc định
            email=ADMIN_EMAIL if ADMIN_EMAIL else "kien0610minh@gmail.com",  # Đảm bảo email không rỗng
            phone="0123456789",  # Số điện thoại mặc định
            position="Admin",  # Chức danh mặc định
            username=ADMIN_USERNAME if ADMIN_USERNAME else "admin",  # Đảm bảo username hợp lệ
            hashed_password=hashed_password,
            email_verified=True  # Mặc định đã xác thực email
        )
        db.add(admin_user)
        db.commit()
        print("✅ Admin account created successfully!")

# Đăng ký tài khoản quản lý mới 
def register_admin(db: Session, admin_data: AdminCreate): 
    if db.query(User).filter(User.email == admin_data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(admin_data.password)
    new_admin = User(
        email = admin_data.email,
        username=admin_data.username,
        hashed_password=hashed_password,
        email_verified=True
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin


# Xác thực user
def authenticate_user(db: Session, email: str, password: str):
    admin = db.query(User).filter(User.email == email).first()
    if not admin or not verify_password(password, admin.hashed_password):
        return None
    return admin

def get_admin_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# Lấy user theo ID
def get_admin_by_id(db: Session, admin_id: int):
    return db.query(User).filter(User.id == admin_id).first()

# Lấy danh sách tất cả (admin)
def get_all_admin(db: Session):
    return db.query(User).all()

# Cập nhật thông tin admin
def update_admin_info(db: Session, admin_id: int, admin_update: AdminUpdate):
    admin = get_admin_by_id(db, admin_id)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    update_data = admin_update.dict(exclude_unset=True)  # Lấy dữ liệu có thay đổi
    for key, value in update_data.items():
        setattr(admin, key, value)  # Cập nhật từng thuộc tính

    db.commit()
    db.refresh(admin)
    return admin

# Gửi mã OTP xác thực email
def send_otp_verification_email(db: Session, email: str):
    admin = get_admin_by_email(db, email)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    
    otp = save_otp(db, admin)
    send_otp_email(email, otp)  # Gửi email OTP

    return {"message": "OTP sent successfully"}


# Xác minh mã OTP
def verify_otp(db: Session, email: str, otp: str):
    admin = get_admin_by_email(db, email)
    if not admin or admin.otp_code != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if admin.otp_expiration < datetime.now(datetime.timezone.utc):
        raise HTTPException(status_code=400, detail="OTP expired")

    admin.email_verified = True
    admin.otp_code = None
    admin.otp_expiration = None
    db.commit()

    return {"message": "Email verified successfully"}

