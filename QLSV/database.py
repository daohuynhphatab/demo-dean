path = r"D:\code\doan\QLSV.txt"

def save(line):
    """Ghi thêm 1 dòng dữ liệu vào file"""
    try:
        with open(path, "a", encoding="utf8") as f:
            f.write(line + "\n")
    except Exception as e:
        print("Lỗi khi ghi file:", e)


def read():
    """Đọc toàn bộ danh sách sinh viên"""
    sv = []
    try:
        with open(path, "r", encoding="utf8") as f:
            for i in f:
                data = i.strip()
                if not data:
                    continue
                arr = data.split("-")
                sv.append(arr)
    except FileNotFoundError:
        open(path, "w", encoding="utf8").close()  # nếu chưa có file thì tạo mới
    except Exception as e:
        print("Lỗi khi đọc file:", e)
    return sv


def overwrite(data_list):
    """Ghi đè toàn bộ danh sách sinh viên"""
    try:
        with open(path, "w", encoding="utf8") as f:
            for sv in data_list:
                f.write("-".join(sv) + "\n")
    except Exception as e:
        print("Lỗi khi ghi đè:", e)
