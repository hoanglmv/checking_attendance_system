import os

def print_directory_tree(startpath, indent=0):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, "").count(os.sep)
        indent_str = "│   " * level + "├── " if level > 0 else ""
        print(f"{indent_str}{os.path.basename(root)}/")
        sub_indent = "│   " * (level + 1)
        for file in files:
            print(f"{sub_indent}├── {file}")

if __name__ == "__main__":
    project_path = "."  # Thư mục hiện tại
    print_directory_tree(project_path)
