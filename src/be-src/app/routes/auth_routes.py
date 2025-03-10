from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.services.auth_service import (
    create_admin_user, authenticate_user, get_admin_by_email, 
    update_admin_info, send_otp_verification_email, verify_otp
)
from app.services.email_service import generate_otp, send_otp_email, save_otp, verify_otp_code
from app.schemas.user_schema import AdminCreate, AdminLogin, AdminUpdate
from app.utils.security import create_access_token
from app.dependencies import get_current_admin

router = APIRouter(prefix="/auth", tags=["Authentication"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Đăng ký tài khoản
@router.post("/register")
def register(admin_data: AdminCreate, db: Session = Depends(get_db)):
    if get_admin_by_email(db, admin_data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    create_admin_user(db, admin_data)
    
    # Gửi OTP sau khi tạo tài khoản
    success, message = send_otp_verification_email(db, admin_data.email)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    return {"message": "Admin registered successfully. Please verify your email with the OTP sent."}

# Xác minh OTP
@router.post("/verify-otp")
def verify_email_otp(email: str, otp: str, db: Session = Depends(get_db)):
    if verify_otp_code(db, email, otp):
        return {"message": "Email verified successfully"}
    raise HTTPException(status_code=400, detail="Invalid or expired OTP")

# Đăng nhập
@router.post("/login")
def login(admin_data: AdminLogin, db: Session = Depends(get_db)):
    admin = authenticate_user(db, admin_data.email, admin_data.password)
    if not admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not admin.email_verified:
        raise HTTPException(status_code=403, detail="Email not verified. Please verify your email first.")
    
    access_token = create_access_token(data={"sub": admin_data.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Lấy thông tin cá nhân
@router.get("/me")
def get_my_info(current_admin: dict = Depends(get_current_admin)):
    return current_admin

# Cập nhật thông tin cá nhân
@router.put("/me/update")
def update_my_info(admin_update: AdminUpdate, db: Session = Depends(get_db), current_admin: dict = Depends(get_current_admin)):
    return update_admin_info(db, current_admin["id"], admin_update)

