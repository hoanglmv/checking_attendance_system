import smtplib
import pytz
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.otp_codes import OTPCode  # Ensure this import is correct
from app.models.user import User
import logging

logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

# Cấu hình SMTP (Cần thay thế bằng thông tin thực tế)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "kien0610minh@gmail.com"
SMTP_PASSWORD = "aedh uvoo fupz madc"

# Gửi email chứa mã OTP
def send_otp_email(email: str, otp: str):
    msg = MIMEText(f"""
        Xin chào,

        Mã OTP của bạn là: {otp}

        Mã này có hiệu lực trong 5 phút. Nếu bạn không yêu cầu, hãy bỏ qua email này.

        Trân trọng,
        Hệ thống Xác thực
    """)
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
        logging.error(f"Failed to send email to {email}: {e}")
        return False, f"Failed to send email: {str(e)}"

# Lưu OTP vào database
def save_otp(db: Session, email: str, otp: str):
    try:
        expires_at = datetime.now() + timedelta(minutes=5)

        # Xóa OTP cũ nếu có
        db.query(OTPCode).filter(OTPCode.email == email).delete()

        otp_entry = OTPCode(email=email, otp=otp, expires_at=expires_at)
        db.add(otp_entry)
        db.commit()

        return True, "OTP saved successfully"
    except SQLAlchemyError as e:
        db.rollback()
        return False, f"Database error: {str(e)}"

# Xác minh mã OTP
def verify_otp_code(db: Session, email: str, otp: str):
    otp_entry = db.query(OTPCode).filter(
        OTPCode.email == email,
        OTPCode.expires_at > datetime.now()
    ).first()

    if not otp_entry:
        return False, "Invalid or expired OTP"

    if otp_entry.otp != otp:
        return False, "Invalid OTP"

    # Đánh dấu email đã xác minh
    user = db.query(User).filter(User.email == email).first()
    if user:
        try:
            user.email_verified = True
            db.commit()
            db.delete(otp_entry)
            db.commit()
            return True, "OTP verified successfully"
        except Exception:
            db.rollback()
            return False, "Database error"

    return False, "User not found"

# Xóa OTP hết hạn
def delete_expired_otps(db: Session):
    try:
        db.query(OTPCode).filter(OTPCode.expires_at < datetime.now()).delete()
        db.commit()
    except SQLAlchemyError:
        db.rollback()