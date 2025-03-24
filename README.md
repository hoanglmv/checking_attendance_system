Checking Attendance System

1. Giới thiệu

Checking Attendance System là hệ thống điểm danh sử dụng nhận diện khuôn mặt, được xây dựng bằng FastAPI, MTCNN, Facenet và MySQL. Hệ thống hỗ trợ hai camera: một cho check-in và một cho check-out, giúp quản lý thời gian làm việc một cách tự động và chính xác.

2. Tính năng chính

Đăng ký khuôn mặt nhân viên và lưu trữ vào cơ sở dữ liệu.

Nhận diện khuôn mặt và ghi nhận điểm danh tự động.

Hỗ trợ hai camera riêng biệt cho check-in và check-out.

Ghi nhận thời gian vào/ra vào bảng attendances trong MySQL.

Giao diện người dùng bằng PyQt6 để quản lý dữ liệu.

3. Công nghệ sử dụng

Backend: FastAPI

Nhận diện khuôn mặt: MTCNN, Facenet

Cơ sở dữ liệu: MySQL

Giao diện người dùng: PyQt6

Camera: OpenCV

4. Cài đặt và triển khai

4.1. Yêu cầu hệ thống

Python 3.10+

MySQL

Các thư viện Python:

pip install fastapi uvicorn numpy opencv-python tensorflow keras pymysql PyQt6

4.2. Cấu hình cơ sở dữ liệu

Tạo cơ sở dữ liệu MySQL:

CREATE DATABASE attendance_system;

Tạo bảng employees và attendances:

CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    face_embedding BLOB NOT NULL
);

CREATE TABLE attendances (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    check_in_time DATETIME,
    check_out_time DATETIME,
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);

4.3. Chạy FastAPI server

uvicorn main:app --reload

4.4. Chạy giao diện PyQt6

python ui.py

5. Sử dụng

Đăng ký khuôn mặt: Nhân viên mới đăng ký khuôn mặt qua UI.

Điểm danh: Camera sẽ nhận diện khuôn mặt và ghi nhận check-in/check-out.

Quản lý dữ liệu: Quản trị viên có thể xem danh sách nhân viên và lịch sử điểm danh.

6. Đóng góp

Nếu bạn muốn đóng góp, hãy fork repo và tạo pull request!

7. Liên hệ

Email: 

GitHub: 

Checking Attendance System - 2025