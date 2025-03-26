import os

def print_dir_structure(startpath, indent=0):
    ignored_dirs = {"venv", "__pycache__"}  # Các thư mục cần bỏ qua
    for item in sorted(os.listdir(startpath)):
        path = os.path.join(startpath, item)
        if item in ignored_dirs:  # Bỏ qua thư mục trong danh sách
            continue
        if os.path.isdir(path):
            print("│   " * indent + "├── 📁 " + item)
            print_dir_structure(path, indent + 1)
        else:
            print("│   " * indent + "├── 📄 " + item)

project_path = r"D:\vhproj\checking_attendance_system\src"
print("📂 checking_attendance_system")
print_dir_structure(project_path)
