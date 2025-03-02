import json
from sqlalchemy.orm import Session
from app.models.user_models import User
from app.schemas.user_schema import UserCreate, UserUpdate
from app.utils.security import get_password_hash, verify_password, save_otp
from app.services.email_service import send_otp_email
from datetime import datetime

# Giá trị mặc định cho role và status
DEFAULT_ROLE = "USER"
DEFAULT_STATUS = "ACTIVE"
ADMIN_ROLE = "ADMIN"
ADMIN_EMAIL = "admin@example.com"  # Email của admin mặc định
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"  # Đổi mật khẩu này sau khi chạy lần đầu

# Tạo tài khoản ADMIN nếu chưa có
def create_admin_user(db: Session):
    admin = db.query(User).filter(User.role == ADMIN_ROLE).first()
    face_embedding_data = json.dumps([]).encode("utf-8")  

    if not admin:
        hashed_password = get_password_hash(ADMIN_PASSWORD)
        admin_user = User(
            name="Administrator",  # Đặt tên mặc định
            email=ADMIN_EMAIL if ADMIN_EMAIL else "kien0610minh@gmail.com",  # Đảm bảo email không rỗng
            phone="0123456789",  # Số điện thoại mặc định
            position="Admin",  # Chức danh mặc định
            profile_image="default_admin.png",  # Ảnh đại diện mặc định
            face_embedding=face_embedding_data,  
            username=ADMIN_USERNAME if ADMIN_USERNAME else "admin",  # Đảm bảo username hợp lệ
            hashed_password=hashed_password,
            role=ADMIN_ROLE,
            status=DEFAULT_STATUS,
            email_verified=True  # Mặc định đã xác thực email
        )
        db.add(admin_user)
        db.commit()
        print("✅ Admin account created successfully!")

# Tạo user mới
def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        role=DEFAULT_ROLE,  # User mặc định có role USER
        status=DEFAULT_STATUS,  # Trạng thái ACTIVE
        email_verified=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Xác thực user
def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

# Lấy user theo email
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# Lấy user theo ID
def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# Lấy danh sách tất cả user (admin)
def get_all_users(db: Session):
    return db.query(User).all()

# Cập nhật thông tin user
def update_user_info(db: Session, user_id: int, user_update: UserUpdate):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

# Gửi mã OTP xác thực email
def send_otp_verification_email(db: Session, email: str):
    user = get_user_by_email(db, email)
    if not user:
        return False, "User not found"
    
    otp = save_otp(db, user)
    
    send_otp_email(email, otp)  # Gọi đúng hàm trong email_service.py

    return True, "OTP sent successfully"

# Xác minh mã OTP
def verify_otp(db: Session, email: str, otp: str):
    user = get_user_by_email(db, email)
    if not user or user.otp_code != otp:
        return False, "Invalid OTP"

    if user.otp_expiration < datetime.utcnow():
        return False, "OTP expired"

    # Xác minh thành công → Cập nhật trạng thái email_verified
    user.email_verified = True
    user.otp_code = None
    user.otp_expiration = None
    db.commit()

    return True, "Email verified successfully"

# ADMIN: Cấp quyền cho user theo userId
def update_user_role(db: Session, admin_id: int, user_id: int, new_role: str):
    admin = get_user_by_id(db, admin_id)
    user = get_user_by_id(db, user_id)

    if not admin or admin.role != ADMIN_ROLE:
        return False, "Only ADMIN can change user roles"

    if not user:
        return False, "User not found"

    user.role = new_role
    db.commit()
    return True, f"User {user.username} role updated to {new_role}"
