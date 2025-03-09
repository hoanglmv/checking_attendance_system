import pymysql

host = "localhost"
user = "root"
password = "hoanglmv"

try:
    connection = pymysql.connect(host=host, user=user, password=password)
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS mlattendance;")
    print("✅ Database 'mlattendance' đã được tạo!")
    connection.close()
except Exception as e:
    print("❌ Lỗi:", e)
