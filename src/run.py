import subprocess
import time

# Chạy Backend
backend_process = subprocess.Popen(
    ["uvicorn", "be-src.app.main:app", "--reload"],
    cwd="E:/AttendanceCheckingApp/checking_attendance_system/src"
)

# Chờ 2 giây để backend khởi động
time.sleep(2)

# Chạy Frontend
frontend_process = subprocess.Popen(
    ["python", "fe/main.py"],
    cwd="E:/AttendanceCheckingApp/checking_attendance_system/src"
)

# Đợi cả hai tiến trình chạy
backend_process.wait()
frontend_process.wait()
