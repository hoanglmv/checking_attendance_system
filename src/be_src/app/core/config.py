import os
from dotenv import load_dotenv
from pydantic import BaseModel

# Load biến môi trường từ .env nếu có
load_dotenv()

# Cấu hình Database
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:123456@localhost/mlattendance")

# Cấu hình bảo mật
SECRET_KEY = os.getenv("SECRET_KEY", "4d419d387f139df1138c501a02eb315e2fcffcadb369e8b7881d6f80cb6f58e8")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Cấu hình SMTP (Email)
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "your_email@gmail.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "your_email_password")
EMAIL_FROM = os.getenv("EMAIL_FROM", SMTP_USERNAME)

class MailConfig(BaseModel):
    MAIL_USERNAME: str = "kien0610minh@gmail.com"
    MAIL_PASSWORD: str = "your_password"
    MAIL_FROM: str = "kien0610minh@gmail.com"
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_PORT: int = 587
    MAIL_TLS: bool = True
    MAIL_SSL: bool = False
