from datetime import datetime
from typing import Optional
from fastapi import APIRouter, BackgroundTasks, Depends, Form, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.services.auth_service import (
    create_admin_user, authenticate_user, get_admin_by_email, request_password_reset, 
    update_admin_info, send_otp_verification_email, verify_otp, register_admin, reset_user_password
)
from app.services.email_service import save_otp, verify_otp_code
from app.schemas.user_schema import AdminCreate, AdminLogin, AdminUpdate, AdminResponse, ForgotPasswordRequest, ResetPasswordRequest
from app.utils.security import create_access_token, generate_otp
from app.utils.dependencies import get_current_admin, CurrentAdmin
from app.models.otp_codes import OTPCode

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
    print(f"📌 Register request: {admin_data}")
    if get_admin_by_email(db, admin_data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_admin = register_admin(db, admin_data, background_tasks)
    return {"message": "Admin registered successfully. Please verify your email with the OTP sent."}

# Xác minh OTP
@router.post("/verify-otp")
def verify_email_otp(email: str, otp: str, db: Session = Depends(get_db)):
    success, message = verify_otp_code(db, email, otp)
    if success:
        return {"message": message}
    raise HTTPException(status_code=400, detail=message)

# Endpoint xác minh OTP cho quên mật khẩu
@router.post("/verify-otp-forgot-password")
def verify_otp_forgot_password(email: str, otp: str, db: Session = Depends(get_db)):
    print(f"Received email: {email}, otp: {otp} for /auth/verify-otp-forgot-password")
    # Kiểm tra OTP
    otp_entry = db.query(OTPCode).filter(
        OTPCode.email == email,
        OTPCode.otp == otp,
        OTPCode.expires_at > datetime.now()
    ).first()

    if not otp_entry:
        print(f"No OTP entry found for email: {email}, otp: {otp}")
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    # Không xóa OTP ở đây, để endpoint /auth/reset-password xử lý
    return {"message": "OTP verified successfully"}

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

    access_token = create_access_token(data={"sub": str(admin.id)})
    admin_response = AdminResponse.model_validate(admin)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "admin": admin_response
    }

# Lấy thông tin cá nhân
@router.get("/me")
def get_my_info(current_admin: CurrentAdmin = Depends(get_current_admin)):
    return current_admin

# Cập nhật thông tin cá nhân
@router.put("/me/update")
async def update_my_info(
    full_name: str = Form(None),
    position: str = Form(None),
    department: str = Form(None),
    phone: str = Form(None),
    db: Session = Depends(get_db), 
    current_admin: CurrentAdmin = Depends(get_current_admin)
):
    print(f"🚀 current_admin: {current_admin}")
    try:
        admin_id = current_admin.id

        update_data = AdminUpdate(
            full_name=full_name,
            position=position,
            department=department,
            phone=phone
        ).model_dump(exclude_unset=True)
        print(f"🚀 update_data: {update_data}")

        if not update_data:
            print("🚫 No fields to update")
            raise HTTPException(status_code=400, detail="No fields to update.")

        if "email" in update_data:
            print("🚫 Cannot update email")
            raise HTTPException(status_code=400, detail="Cannot update email.")

        updated_admin = update_admin_info(db, admin_id, AdminUpdate(**update_data))

        return {
            "message": "Admin info updated successfully",
            "updated_data": updated_admin
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"🚫 Lỗi không xác định trong update_my_info: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/logout")
def logout(current_admin: CurrentAdmin = Depends(get_current_admin)):
    """
    Đăng xuất người dùng. 
    - Backend: Chỉ kiểm tra xem người dùng có đang đăng nhập không.
    - Frontend: Xóa access_token khỏi QSettings.
    """
    return {"message": "Logged out successfully"}

@router.post("/forgot-password")
def forgot_password(
    request: ForgotPasswordRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    success, message = request_password_reset(db, request.email)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    return {"message": "OTP has been sent to your email. Please verify to reset your password."}

@router.post("/reset-password")
def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    print(f"Calling reset_user_password with email: {request.email}, otp: {request.otp}, new_password: {request.new_password}")
    success, message = reset_user_password(db, request.email, request.otp, request.new_password)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    return {"message": "Password has been reset successfully"}