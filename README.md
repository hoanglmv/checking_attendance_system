# Checking Attendance System

## 1. Giới thiệu

**Checking Attendance System** là hệ thống điểm danh sử dụng nhận diện khuôn mặt, được xây dựng bằng **FastAPI**, **MTCNN**, **FaceNet**, và **MySQL**. Hệ thống hỗ trợ hai camera: một cho **check-in** và một cho **check-out**, giúp quản lý thời gian làm việc một cách tự động và chính xác.

## 2. Tính năng chính

- Đăng ký khuôn mặt nhân viên và lưu trữ vào cơ sở dữ liệu.
- Nhận diện khuôn mặt và ghi nhận điểm danh tự động.
- Hỗ trợ hai camera riêng biệt cho **check-in** và **check-out**.
- Ghi nhận thời gian vào/ra vào bảng `attendances` trong MySQL.
- Giao diện người dùng bằng **PyQt6** để quản lý dữ liệu.

## 3. Công nghệ sử dụng

- **Backend**: FastAPI
- **Nhận diện khuôn mặt**: MTCNN, FaceNet
- **Cơ sở dữ liệu**: MySQL
- **Giao diện người dùng**: PyQt6
- **Xử lý hình ảnh**: OpenCV

## 4. Cài đặt và triển khai

### 4.1. Yêu cầu hệ thống

- **Python**: 3.10+
- **MySQL**
- Các thư viện Python (cài đặt bằng `pip`):
  ```bash
  pip install fastapi uvicorn numpy opencv-python tensorflow keras pymysql PyQt6