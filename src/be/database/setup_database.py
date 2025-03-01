from database import Database

# Khởi tạo đối tượng database
db = Database()

# Tạo bảng employees
db.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(20),
    position VARCHAR(100),
    profile_image TEXT,
    face_embedding BLOB
)
""")

# Tạo bảng attendance
db.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    checkin_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE
)
""")

print("🎉 Cơ sở dữ liệu đã được thiết lập xong!")
db.close()
# chạy trong terminal lệnh : python setup_database.py
