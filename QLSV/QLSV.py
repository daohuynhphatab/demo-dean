import tkinter as tk
from tkinter import messagebox, Listbox, Entry, Frame, Button, Label, W, E
import mysql.connector

# Kết nối đến cơ sở dữ liệu
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  
            password='123456', 
            database='qlsv'
        )
        return connection
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
        return None

# Hàm thêm sinh viên
def add_student():
    student_id = entry_id.get()
    name = entry_name.get()
    date = entry_date.get()
    address = entry_address.get()
    class_id = entry_classid.get()
    
    # Kiểm tra dữ liệu nhập vào
    if not student_id or not name:
        messagebox.showwarning("Input Error", "Vui lòng nhập đầy đủ thông tin")
        return
    
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            sql = "INSERT INTO sinhvien (id, name, date, address, classid) VALUES (%s, %s, %s, %s, %s)"
            values = (student_id, name, date, address, class_id)
            cursor.execute(sql, values)
            connection.commit()
            messagebox.showinfo("Success", f"Thêm sinh viên {name} thành công")

            # Thêm vào listbox
            listbox.insert(tk.END, f"{student_id} - {name}")

            # Xóa trường nhập
            clear_entries()

        except Exception as e:
            messagebox.showerror("Database Error", "Failed to add student: " + str(e))
        finally:
            cursor.close()
            connection.close()

def clear_entries():
    entry_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_date.delete(0, tk.END)
    entry_address.delete(0, tk.END)
    entry_classid.delete(0, tk.END)

# Hàm xóa sinh viên
def delete_student():
    selected_student = listbox.curselection()
    if not selected_student:
        messagebox.showwarning("Selection Error", "Vui lòng chọn sinh viên để xóa")
        return
    
    student_info = listbox.get(selected_student)
    student_id = student_info.split(" - ")[0]  # Lấy ID từ danh sách
    
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            sql = "DELETE FROM sinhvien WHERE id = %s"
            cursor.execute(sql, (student_id,))
            connection.commit()
            messagebox.showinfo("Success", f"Đã xóa sinh viên có mã {student_id}")

            # Cập nhật danh sách sinh viên
            listbox.delete(selected_student)
            
        except Exception as e:
            messagebox.showerror("Database Error", "Failed to delete student: " + str(e))
        finally:
            cursor.close()
            connection.close()

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Quản Lý Sinh Viên")

# Tiêu đề
Label(root, text="Quản Lý Sinh Viên", font=("Arial", 24)).grid(row=0, columnspan=2, pady=10)

# Danh sách sinh viên
listbox = Listbox(root, width=80, height=20)
listbox.grid(row=1, columnspan=2)

# Trường nhập Mã sinh viên
Label(root, text="Mã sinh viên:").grid(row=2, column=0, sticky=W, padx=10)
entry_id = Entry(root, width=30)
entry_id.grid(row=2, column=1, sticky=W)

# Trường nhập Họ và tên
Label(root, text="Họ và tên:").grid(row=3, column=0, sticky=W, padx=10)
entry_name = Entry(root, width=30)
entry_name.grid(row=3, column=1, sticky=W)

# Trường nhập năm sinh
Label(root, text="Năm sinh:").grid(row=4, column=0, sticky=W, padx=10)
entry_date = Entry(root, width=30)
entry_date.grid(row=4, column=1, sticky=W)

# Trường nhập địa chỉ
Label(root, text="Địa chỉ:").grid(row=5, column=0, sticky=W, padx=10)
entry_address = Entry(root, width=30)
entry_address.grid(row=5, column=1, sticky=W)

# Trường nhập mã lớp
Label(root, text="Mã lớp học:").grid(row=6, column=0, sticky=W, padx=10)
entry_classid = Entry(root, width=30)
entry_classid.grid(row=6, column=1, sticky=W)

# Khung chứa nút
frame_btn = Frame(root)
frame_btn.grid(row=7, column=1, pady=15, sticky=E)

# Nút thêm
Button(frame_btn, text="Thêm", command=add_student, width=10).pack(side='left', padx=5)

# Nút xóa
Button(frame_btn, text="Xóa", command=delete_student, width=10).pack(side='left', padx=5)

# Nút sửa (chưa có code)
Button(frame_btn, text="Sửa", width=10).pack(side='left', padx=5)

# Nút thoát
Button(frame_btn, text="Thoát", command=root.quit, width=10).pack(side='left', padx=5)

# Chạy ứng dụng
root.mainloop()