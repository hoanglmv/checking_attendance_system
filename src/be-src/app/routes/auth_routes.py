from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.services.auth_service import (
    create_admin_user, authenticate_user, get_admin_by_email, 
    update_admin_info, send_otp_verification_email, verify_otp, register_admin
)

from app.services.email_service import save_otp, verify_otp_code
from app.schemas.user_schema import AdminCreate, AdminLogin, AdminUpdate
from app.utils.security import create_access_token, generate_otp
from app.utils.dependencies import get_current_admin

router = APIRouter(prefix="/auth", tags=["Authentication"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Đăng ký tài khoản
@router.post("/register")
def register(admin_data: AdminCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    print(f"📌 Register request: {admin_data}")  # Debug log

    if get_admin_by_email(db, admin_data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Tạo admin và gửi OTP trong cùng một hàm
    new_admin = register_admin(db, admin_data, background_tasks)

    return {"message": "Admin registered successfully. Please verify your email with the OTP sent."}

# Xác minh OTP
@router.post("/verify-otp")
def verify_email_otp(email: str, otp: str, db: Session = Depends(get_db)):
    success, message = verify_otp_code(db, email, otp)
    if success:
        return {"message": message}
    raise HTTPException(status_code=400, detail=message)

# Đăng nhập
@router.post("/login")
def login(admin_data: AdminLogin, db: Session = Depends(get_db)):
    admin = authenticate_user(db, admin_data.email, admin_data.password)
    if not admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not admin.email_verified:
        raise HTTPException(status_code=403, detail="Email not verified. Please verify your email first.")
    
    print(f"🆔 Admin ID: {admin.id}")  
    print(f"📧 Admin Email: {admin.email}")

    access_token = create_access_token(data={"sub": str(admin.id)})  # Đảm bảo sub chứa admin.id

    return {"access_token": access_token, "token_type": "bearer"}

# Lấy thông tin cá nhân
@router.get("/me")
def get_my_info(current_admin: dict = Depends(get_current_admin)):
    return current_admin

# Cập nhật thông tin cá nhân
@router.put("/me/update")
def update_my_info(
    admin_update: AdminUpdate, 
    db: Session = Depends(get_db), 
    current_admin: dict = Depends(get_current_admin)
):
    # Kiểm tra nếu không có dữ liệu cần cập nhật
    update_data = admin_update.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update.")

    # Không cho phép cập nhật email
    if "email" in update_data:
        raise HTTPException(status_code=400, detail="Cannot update email.")

    # Thực hiện cập nhật thông tin
    updated_admin = update_admin_info(db, current_admin.id, admin_update)

    return {
        "message": "Admin info updated successfully",
        "updated_data": updated_admin
    }
