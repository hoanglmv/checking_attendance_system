from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.services.user_service import (
    create_user, get_user_by_email, authenticate_user, get_user_by_id, 
    update_user_info, get_all_users
)
from app.services.email_service import generate_otp, send_otp_email, save_otp, verify_otp_code
from app.schemas.user_schema import UserCreate, UserLogin, UserUpdate
from app.utils.security import create_access_token
from app.dependencies import get_current_user, get_current_admin

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Đăng ký tài khoản
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    created_user = create_user(db, user)
    
    # Gửi OTP sau khi tạo tài khoản
    otp = generate_otp()
    send_otp_email(user.email, otp)
    save_otp(db, user.email, otp)
    
    return {"message": "User registered successfully. Please verify your email with the OTP sent."}

# Xác minh OTP
@router.post("/verify-otp")
def verify_email_otp(email: str, otp: str, db: Session = Depends(get_db)):
    if verify_otp_code(db, email, otp):
        return {"message": "Email verified successfully"}
    raise HTTPException(status_code=400, detail="Invalid or expired OTP")

# Đăng nhập
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not db_user.email_verified:
        raise HTTPException(status_code=403, detail="Email not verified. Please verify your email first.")
    
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Lấy thông tin cá nhân
@router.get("/me")
def get_my_info(current_user: dict = Depends(get_current_user)):
    return current_user

# Cập nhật thông tin cá nhân
@router.put("/me/update")
def update_my_info(user_update: UserUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return update_user_info(db, current_user["id"], user_update)

# Admin: Lấy thông tin user theo ID
@router.get("/{user_id}")
def get_user_by_admin(user_id: int, db: Session = Depends(get_db), admin: dict = Depends(get_current_admin)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Admin: Lấy danh sách tất cả user
@router.get("/")
def get_all_users_list(db: Session = Depends(get_db), admin: dict = Depends(get_current_admin)):
    return get_all_users(db)

# Admin: Cập nhật thông tin user theo ID
@router.put("/{user_id}/update")
def update_user_by_admin(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db), admin: dict = Depends(get_current_admin)):
    return update_user_info(db, user_id, user_update)
