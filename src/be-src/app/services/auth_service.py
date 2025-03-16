import json
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.otp_codes import OTPCode
from app.schemas.user_schema import AdminCreate, AdminUpdate
from app.utils.security import get_password_hash, verify_password, generate_otp
from app.services.email_service import  send_otp_email, save_otp
from fastapi import BackgroundTasks, HTTPException
from datetime import datetime, timedelta
import pytz
import sys
sys.stdout.reconfigure(encoding='utf-8')

ADMIN_EMAIL = "admin@example.com"  # Email của admin mặc định
ADMIN_PASSWORD = "admin123"  # Đổi mật khẩu này sau khi chạy lần đầu

# Tạo tài khoản ADMIN nếu chưa có
def create_admin_user(db: Session):
    admin = db.query(User).first()

    if not admin:
        hashed_password = get_password_hash(ADMIN_PASSWORD)
        admin_user = User(
            full_name="Administrator",
            email=ADMIN_EMAIL,
            phone="0123456789",
            position="Admin",
            department="Management",  # Thêm department mặc định
            hashed_password=hashed_password,
            is_admin=True,  # Đánh dấu là admin
            email_verified=True
        )
        db.add(admin_user)
        db.commit()
        print("✅ Admin account created successfully!")

# Đăng ký tài khoản quản lý mới 
def register_admin(db: Session, admin_data: AdminCreate, background_tasks: BackgroundTasks): 
    if db.query(User).filter(User.email == admin_data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(admin_data.password)
    new_admin = User(
        full_name=admin_data.full_name,
        email=admin_data.email,
        phone=admin_data.phone,
        position=admin_data.position,
        department=admin_data.department,
        hashed_password=hashed_password,
        email_verified=False,
        is_admin = True,
        created_at=datetime.now()  # ✅ Đảm bảo có timestamp chính xác
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    

    # Gửi OTP để xác thực email
    success, message = send_otp_verification_email(db, admin_data.email)
    if not success:
        raise HTTPException(status_code=400, detail=message)

    # ✅ Thêm task tự động xóa nếu chưa xác thực sau 5 phút
    background_tasks.add_task(delete_unverified_accounts, db)

    return {"message": "Admin registered successfully. Please verify your email with the OTP sent."}
# Xác thực user
def authenticate_user(db: Session, email: str, password: str):
    admin = db.query(User).filter(User.email == email).first()
    if not admin or not verify_password(password, admin.hashed_password):
        return None
    if not admin.email_verified:  # Kiểm tra trạng thái xác thực email
        return None  # Không cho phép đăng nhập
    print(f"✅ Authenticated Admin: ID={admin.id}, Email={admin.email}")

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
    otp = generate_otp()  # ✅ Tạo OTP trước
    success, message = save_otp(db, email, otp)  # ✅ Lưu OTP đúng cách
    if not success:
        return False, message  # Lưu thất bại

    send_otp_email(email, otp)  # ✅ Gửi OTP qua email

    return True, "OTP sent successfully"


# Xác minh mã OTP
# Xác minh mã OTP
def verify_otp(db: Session, email: str, otp: str):
    admin = get_admin_by_email(db, email)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    otp_record = db.query(OTPCode).filter(
        OTPCode.user_id == admin.id,
        OTPCode.otp == otp
    ).first()

    if not otp_record:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if otp_record.expiration < datetime.now():  
        db.delete(otp_record)
        db.commit()
        raise HTTPException(status_code=400, detail="OTP expired")

    admin.email_verified = True
    db.delete(otp_record)
    db.commit()

    return {"message": "Email verified successfully"}

# Xoá tài khoản sau 5p chưa xác thực OTP
def delete_unverified_accounts(db: Session):
    time_threshold = datetime.now() - timedelta(minutes=5)
    unverified_users = db.query(User).filter(
        User.email_verified == False,
        User.created_at < time_threshold
    ).all()

    for user in unverified_users:
        db.delete(user)

    db.commit()
