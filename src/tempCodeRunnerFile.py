import subprocess
import time

# Chạy Backend
backend_process = subprocess.Popen(
    ["uvicorn", "be_src.app.main:app", "--reload"],
    cwd="D://NMCNPM//checking_attendance_system\src"
)

# Chờ 2 giây để backend khởi động
time.sleep(1)

# Chạy Frontend
frontend_process = subprocess.Popen(
    ["python", "fe/main.py"],
    cwd="D://NMCNPM//checking_attendance_system\src"
)

backend_process.wait()
frontend_process.wait()
