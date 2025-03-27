FROM python:3.10

WORKDIR /app

# Cập nhật hệ thống và cài đặt thư viện hệ thống cần thiết cho GUI qua X11
RUN apt-get update && apt-get install -y \
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

# Chạy ứng dụng GUI (run.py nằm trong /app/src)
CMD ["python", "src/run.py"]
