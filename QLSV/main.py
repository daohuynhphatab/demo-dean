import tkinter as tk
from tkinter import Listbox, Entry, Frame, Button, Label
from QLSV import *
from KHOA import *
from LOP import *

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Quản Lý Sinh Viên")

# Tiêu đề
Label(root, text="Quản Lý Sinh Viên", font=("Arial", 24)).grid(row=0, columnspan=2, pady=10)

# Danh sách sinh viên
listbox = Listbox(root, width=80, height=10)
listbox.grid(row=1, columnspan=2)

# Các thành phần nhập cho sinh viên
# Mã sinh viên
Label(root, text="Mã sinh viên:").grid(row=2, column=0, sticky=tk.W, padx=10)
entry_id = Entry(root, width=30)
entry_id.grid(row=2, column=1, sticky=tk.W)

# Họ và tên
Label(root, text="Họ và tên:").grid(row=3, column=0, sticky=tk.W, padx=10)
entry_name = Entry(root, width=30)
entry_name.grid(row=3, column=1, sticky=tk.W)

# Năm sinh
Label(root, text="Năm sinh:").grid(row=4, column=0, sticky=tk.W, padx=10)
entry_date = Entry(root, width=30)
entry_date.grid(row=4, column=1, sticky=tk.W)

# Địa chỉ
Label(root, text="Địa chỉ:").grid(row=5, column=0, sticky=tk.W, padx=10)
entry_address = Entry(root, width=30)
entry_address.grid(row=5, column=1, sticky=tk.W)

# Mã lớp
Label(root, text="Mã lớp học:").grid(row=6, column=0, sticky=tk.W, padx=10)
entry_classid = Entry(root, width=30)
entry_classid.grid(row=6, column=1, sticky=tk.W)

# Khung chứa nút
frame_btn = Frame(root)
frame_btn.grid(row=7, column=1, pady=15, sticky=tk.E)
 
# Nút thêm
Button(frame_btn, text="Thêm", command=lambda: add_student(entry_id, entry_name, entry_date, entry_address, entry_classid, listbox), width=10).pack(side='left', padx=5)

# Nút xóa
Button(frame_btn, text="Xóa", command=lambda: delete_student(listbox), width=10).pack(side='left', padx=5)

# Nút sửa
Button(frame_btn, text="Sửa", command=lambda: edit_student(listbox, entry_id, entry_name, entry_date, entry_address, entry_classid), width=10).pack(side='left', padx=5)

# Nút Khoa
Button(frame_btn, text="Khoa", command=open_department_management, width=10).pack(side='left', padx=5)

# Nút Lớp học
Button(frame_btn, text="Lớp học", command=open_class_management, width=10).pack(side='left', padx=5)

# Nút thoát
Button(frame_btn, text="Thoát", command=root.quit, width=10).pack(side='left', padx=5)

# Chạy ứng dụng
root.mainloop()