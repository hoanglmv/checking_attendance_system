import random
import string
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import SECRET_KEY, ALGORITHM

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta if expires_delta else timedelta(minutes=30))
    to_encode.update({"exp": expire})
    
    print(f"🛠 Creating token with payload: {to_encode}")  # Debug
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ✅ Chuyển generate_otp() vào đây để tránh xung đột
def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"🔍 Token payload: {payload}")  # Debug log
        return payload
    except JWTError as e:
        print(f"🔴 JWT Error: {e}")  # Debug log
        return None
