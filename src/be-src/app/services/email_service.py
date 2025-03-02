import smtplib
import random
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.otp_codes import OTPCode  # Đúng
  # Đảm bảo model nằm trong đúng module

# Cấu hình SMTP (Cần thay thế thông tin email thật)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "your-email@gmail.com"
SMTP_PASSWORD = "your-app-password"

# Tạo mã OTP 6 chữ số
def generate_otp():
    return str(random.randint(100000, 999999))

# Gửi email chứa mã OTP
def send_otp_email(email: str, otp: str):
    msg = MIMEText(f"Mã OTP của bạn là: {otp}. Mã này sẽ hết hạn sau 5 phút.")
    msg["Subject"] = "Xác thực email"
    msg["From"] = SMTP_USERNAME
    msg["To"] = email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SMTP_USERNAME, email, msg.as_string())
        return True, "OTP sent successfully"
    except smtplib.SMTPException as e:
        return False, f"Failed to send email: {str(e)}"

# Lưu OTP vào database, xóa OTP cũ nếu có
def save_otp(db: Session, email: str, otp: str):
    try:
        # Xóa OTP cũ nếu có
        db.query(OTPCode).filter(OTPCode.email == email).delete()
        
        # Lưu OTP mới
        expires_at = datetime.utcnow() + timedelta(minutes=5)
        otp_entry = OTPCode(email=email, otp=otp, expires_at=expires_at)
        db.add(otp_entry)
        db.commit()
        return True, "OTP saved successfully"
    except SQLAlchemyError as e:
        db.rollback()
        return False, f"Database error: {str(e)}"

# Kiểm tra OTP hợp lệ
def verify_otp_code(db: Session, email: str, otp: str):
    otp_entry = db.query(OTPCode).filter(OTPCode.email == email, OTPCode.otp == otp).first()
    
    if not otp_entry:
        return False, "Invalid OTP"
    
    if otp_entry.expires_at < datetime.utcnow():
        return False, "OTP expired"
    
    # Xác minh thành công → Xóa OTP sau khi dùng
    db.delete(otp_entry)
    db.commit()

    return True, "OTP verified successfully"

# Xóa OTP hết hạn để tránh database bị đầy
def delete_expired_otps(db: Session):
    try:
        db.query(OTPCode).filter(OTPCode.expires_at < datetime.utcnow()).delete()
        db.commit()
    except SQLAlchemyError:
        db.rollback()
