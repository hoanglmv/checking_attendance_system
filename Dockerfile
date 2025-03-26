FROM python:3.10

WORKDIR /app

# Cập nhật hệ thống và cài đặt thư viện hệ thống cần thiết (bao gồm Xvfb và các thư viện hỗ trợ cho PyQt6)
RUN apt-get update && apt-get install -y \
    xvfb \
    libxkbcommon-x11-0 \
    libegl1-mesa \
    libqt6gui6 \
    libqt6widgets6 \
    libqt6core6 \
    libqt6network6 \
    && rm -rf /var/lib/apt/lists/*

# Sao chép thư mục chứa mã nguồn và dữ liệu
COPY src /app/src
COPY data /app/data

# Sao chép và cài đặt dependencies (chỉ chứa các thư viện Python)
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 8000

# Chạy Xvfb và sau đó chạy ứng dụng (run.py nằm trong /app/src)
CMD ["sh", "-c", "Xvfb :99 -screen 0 1920x1080x24 & export DISPLAY=:99 && python src/run.py"]
