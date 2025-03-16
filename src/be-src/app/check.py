from datetime import datetime, timezone
import pytz

print("UTC Time:", datetime.now(timezone.utc))  # Giờ UTC thực tế
print("System Local Time:", datetime.now())  # Giờ theo hệ thống
print("Asia/Ho_Chi_Minh Time:", datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')))  # Giờ Việt Nam
