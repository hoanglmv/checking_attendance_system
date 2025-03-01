import mysql.connector

class Database:
    def __init__(self, host="localhost", user="root", password="yourpassword", database="attendance_db"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None

    def connect(self):
        """Kết nối đến MySQL Database"""
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.conn.cursor()

    def close(self):
        """Đóng kết nối"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def execute(self, query, params=None):
        """Thực thi câu lệnh SQL"""
        self.connect()
        self.cursor.execute(query, params or ())
        self.conn.commit()
        self.close()

    def fetch(self, query, params=None):
        """Truy vấn dữ liệu"""
        self.connect()
        self.cursor.execute(query, params or ())
        result = self.cursor.fetchall()
        self.close()
        return result
