import random
import string
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import SECRET_KEY, ALGORITHM
from sqlalchemy.orm import Session
from app.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=30))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Tạo mã OTP ngẫu nhiên (6 chữ số)
def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

# Lưu mã OTP vào database
def save_otp(db: Session, user: User):
    otp = generate_otp()
    user.otp_code = otp
    user.otp_expiration = datetime.utcnow() + timedelta(minutes=10)  # OTP hết hạn sau 10 phút
    db.commit()
    return otp

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None