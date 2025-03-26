FROM python:3.10

WORKDIR /app

# Sao chép thư mục chứa mã nguồn và dữ liệu
COPY src /app/src
COPY data /app/data

# Sao chép và cài đặt dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 8000

# Chạy ứng dụng, với run.py nằm trong /app/src
CMD ["python", "src/run.py"]
