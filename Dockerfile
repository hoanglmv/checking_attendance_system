# Sử dụng Python 3.10 làm base image
FROM python:3.10

# Đặt thư mục làm việc trong container
WORKDIR /app

# Sao chép tất cả các file vào container
COPY . /app

# Cài đặt các thư viện cần thiết
RUN pip install --no-cache-dir -r requirements.txt

# Expose cổng mà FastAPI sử dụng (thường là 8000)
EXPOSE 8000

# Chạy ứng dụng FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
