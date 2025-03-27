FROM python:3.10

WORKDIR /app

# Cập nhật hệ thống và cài đặt các thư viện cần thiết
RUN apt-get update && apt-get install -y \
    xvfb \
    libxkbcommon-x11-0 \
    libegl1-mesa \
    libqt6gui6 \
    libqt6widgets6 \
    libqt6core6 \
    libqt6network6 \
    libgl1-mesa-glx \
    libxcb1 libx11-xcb1 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-render-util0 \
    && rm -rf /var/lib/apt/lists/*

# Sao chép mã nguồn và dữ liệu
COPY src /app/src
COPY data /app/data

# Sao chép và cài đặt dependencies cho Python
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 8000

# Xoá file khóa của Xvfb, khởi động Xvfb trên display :99, sau đó chạy ứng dụng
CMD ["sh", "-c", "rm -f /tmp/.X99-lock; Xvfb :99 -screen 0 1920x1080x24 & export DISPLAY=:99 && python src/run.py"]
