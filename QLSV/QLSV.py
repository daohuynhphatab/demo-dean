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
            listbox.insert(tk.END, f"{student_id} - {name}")
            clear_entries()
        except Exception as e:
            messagebox.showerror("Database Error", "Failed to add student: " + str(e))
        finally:
            cursor.close()
            connection.close()

# Hàm sửa sinh viên
def edit_student():
    selected_student = listbox.curselection()
    if not selected_student:
        messagebox.showwarning("Selection Error", "Vui lòng chọn sinh viên để sửa")
        return
    
    student_info = listbox.get(selected_student)
    student_id = student_info.split(" - ")[0]
    name = entry_name.get()
    date = entry_date.get()
    address = entry_address.get()
    class_id = entry_classid.get()
    
    if not name:
        messagebox.showwarning("Input Error", "Vui lòng nhập tên sinh viên")
        return

    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            sql = "UPDATE sinhvien SET name=%s, date=%s, address=%s, classid=%s WHERE id=%s"
            values = (name, date, address, class_id, student_id)
            cursor.execute(sql, values)
            connection.commit()
            messagebox.showinfo("Success", f"Sửa sinh viên {student_id} thành công")
            listbox.delete(selected_student)
            listbox.insert(selected_student, f"{student_id} - {name}")
        except Exception as e:
            messagebox.showerror("Database Error", "Failed to edit student: " + str(e))
        finally:
            cursor.close()
            connection.close()

# Hàm xóa sinh viên
def delete_student():
    selected_student = listbox.curselection()
    if not selected_student:
        messagebox.showwarning("Selection Error", "Vui lòng chọn sinh viên để xóa")
        return
    
    student_info = listbox.get(selected_student)
    student_id = student_info.split(" - ")[0]
    
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            sql = "DELETE FROM sinhvien WHERE id = %s"
            cursor.execute(sql, (student_id,))
            connection.commit()
            messagebox.showinfo("Success", f"Đã xóa sinh viên có mã {student_id}")
            listbox.delete(selected_student)
        except Exception as e:
            messagebox.showerror("Database Error", "Failed to delete student: " + str(e))
        finally:
            cursor.close()
            connection.close()

def clear_entries():
    entry_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_date.delete(0, tk.END)
    entry_address.delete(0, tk.END)
    entry_classid.delete(0, tk.END)

# Giao diện quản lý môn học
def open_subject_management():
    subject_window = tk.Toplevel(root)
    subject_window.title("Quản Lý Môn Học")

    # Tiêu đề
    Label(subject_window, text="Quản Lý Môn Học", font=("Arial", 20)).grid(row=0, columnspan=2, pady=10)

    # Danh sách môn học
    subject_listbox = Listbox(subject_window, width=80, height=10)
    subject_listbox.grid(row=1, columnspan=2)

    # Trường nhập Mã môn học
    Label(subject_window, text="Mã môn học:").grid(row=2, column=0, sticky=W, padx=10)
    entry_subject_id = Entry(subject_window, width=30)
    entry_subject_id.grid(row=2, column=1, sticky=W)

    # Trường nhập Tên môn học
    Label(subject_window, text="Tên môn học:").grid(row=3, column=0, sticky=W, padx=10)
    entry_subject_name = Entry(subject_window, width=30)
    entry_subject_name.grid(row=3, column=1, sticky=W)
    
    # Trường nhập Số tín chỉ
    Label(subject_window, text="Số tín chỉ môn học:").grid(row=4, column=0, sticky=W, padx=10)
    entry_subject_TC = Entry(subject_window, width=30)
    entry_subject_TC.grid(row=4, column=1, sticky=W)

    # Hàm thêm môn học
    def add_subject():
        subject_id = entry_subject_id.get()
        subject_name = entry_subject_name.get()
        subject_TC = entry_subject_TC.get()
        
        if not subject_id or not subject_name:
            messagebox.showwarning("Input Error", "Vui lòng nhập đầy đủ thông tin về môn học")
            return

        connection = connect_to_db()
        if connection:
            try:
                cursor = connection.cursor()
                sql = "INSERT INTO monhoc (id, name, tc) VALUES (%s, %s, %s)"
                values = (subject_id, subject_name, subject_TC)
                cursor.execute(sql, values)
                connection.commit()
                messagebox.showinfo("Success", f"Thêm môn học {subject_name} thành công")
                subject_listbox.insert(tk.END, f"{subject_id} - {subject_name} - {subject_TC}")
                clear_subject_entries()
            except Exception as e:
                messagebox.showerror("Database Error", "Failed to add subject: " + str(e))
            finally:
                cursor.close()
                connection.close()

    def clear_subject_entries():
        entry_subject_id.delete(0, tk.END)
        entry_subject_name.delete(0, tk.END)
        entry_subject_TC.delete(0, tk.END)

    # Hàm xóa môn học
    def delete_subject():
        selected_subject = listbox.curselection()
        if not selected_subject:
            messagebox.showwarning("Selection Error", "Vui lòng chọn môn học để xóa")
            return
    
            subject_info = listbox.get(selected_subject)
            subject_id = subject_info.split(" - ")[0]
    
        connection = connect_to_db()
        if connection:
            try:
                cursor = connection.cursor()
                sql = "DELETE FROM monhoc WHERE id = %s"
                cursor.execute(sql, (subject_id,))
                connection.commit()
                messagebox.showinfo("Success", f"Đã xóa môn học có mã {subject_id}")
                listbox.delete(selected_subject)
            except Exception as e:
                messagebox.showerror("Database Error", "Failed to delete subject: " + str(e))
            finally:
                cursor.close()
                connection.close()

    def clear_subject_entries():
        entry_subject_id.delete(0, tk.END)
        entry_subject_name.delete(0, tk.END)
        entry_subject_TC.delete(0, tk.END)


# Nút thêm môn học
    Button(subject_window, text="Thêm Môn Học", command=add_subject, width=15).grid(row=4, columnspan=2, pady=10)
# Nút xóa môn học
    Button(subject_window, text="Xóa Môn Học", command=delete_subject, width=15).grid(row=5, columnspan=2, pady=10)

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Quản Lý Sinh Viên")

# Tiêu đề
Label(root, text="Quản Lý Sinh Viên", font=("Arial", 24)).grid(row=0, columnspan=2, pady=10)

# Danh sách sinh viên
listbox = Listbox(root, width=80, height=10)
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

# Nút sửa
Button(frame_btn, text="Sửa", command=edit_student, width=10).pack(side='left', padx=5)

# Nút Môn học
Button(frame_btn, text="Môn học", command=open_subject_management, width=10).pack(side='left', padx=5)

# Nút thoát
Button(frame_btn, text="Thoát", command=root.quit, width=10).pack(side='left', padx=5)

# Chạy ứng dụng
root.mainloop()