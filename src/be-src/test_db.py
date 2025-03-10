import sys
sys.stdout.reconfigure(encoding='utf-8')
import pymysql

host = "localhost"
user = "root"
password = "hoanglmv"
database = "mlattendance"

try:
    connection = pymysql.connect(host=host, user=user, password=password, database=database)
    print("✅ Kết nối MySQL thành công!")
    connection.close()
except Exception as e:
    print("❌ Lỗi kết nối MySQL:", e)

