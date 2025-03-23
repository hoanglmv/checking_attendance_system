from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from pydantic import BaseModel, EmailStr
from typing import Optional
from app.core.database import SessionLocal
from app.core.config import SECRET_KEY, ALGORITHM
from app.models.user import User 
from app.utils.security import verify_token

# Định nghĩa Pydantic model cho CurrentAdmin
class CurrentAdmin(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    phone: Optional[str] = None  # Có thể null trong model User
    position: Optional[str] = None  # Có thể null trong model User
    department: str

    class Config:
        from_attributes = True  # Cho phép chuyển đổi từ SQLAlchemy model

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> CurrentAdmin:
    print(f"🚀 Verifying token: {token[:10]}...")
    payload = verify_token(token)
    if not payload or "sub" not in payload:
        print("🚫 Invalid token payload or missing 'sub'")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        admin_id = int(payload.get("sub"))
        print(f"🚀 Extracted admin_id from token: {admin_id}")
    except ValueError:
        print("🚫 Invalid token payload: 'sub' is not an integer")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token payload",
        )

    admin = db.query(User).filter(User.id == admin_id, User.is_admin == True).first()
    if not admin:
        print(f"🚫 Admin not found or not authorized for admin_id: {admin_id}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin not found or not authorized",
            headers={"WWW-Authenticate": "Bearer"},
        )

    print(f"🚀 Found admin: id={admin.id}, email={admin.email}, is_admin={admin.is_admin}")
    
    # Chuyển đổi admin thành CurrentAdmin
    current_admin = CurrentAdmin.model_validate(admin)
    print(f"🚀 Returning current_admin: {current_admin}")
    return current_admin