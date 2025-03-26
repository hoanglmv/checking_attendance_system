import os
import ast

def find_imports_in_file(filename):
    """Phân tích một file Python và trích xuất các import."""
    with open(filename, "r", encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read(), filename=filename)
        except Exception as e:
            print(f"Lỗi khi phân tích {filename}: {e}")
            return set()
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                # Lấy phần đầu tiên của tên module, ví dụ: numpy trong numpy.linalg
                imports.add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module is not None:
                imports.add(node.module.split('.')[0])
    return imports

def find_all_imports(directory):
    """Quét tất cả các file Python trong thư mục và trả về danh sách các thư viện được import."""
    all_imports = set()
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                imports = find_imports_in_file(filepath)
                all_imports.update(imports)
    return all_imports

if __name__ == '__main__':
    # Thay đổi đường dẫn theo thư mục dự án của bạn
    project_directory = '.'  # Hoặc đường dẫn cụ thể của dự án
    imports = find_all_imports(project_directory)
    print("Các thư viện được import trong dự án:")
    for lib in sorted(imports):
        print(lib)
