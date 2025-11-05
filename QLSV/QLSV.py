from database import connect_to_db
import tkinter as tk
from tkinter import messagebox, Listbox, Entry, Frame, Button, Label, W, E
 


def add_student(entry_id, entry_name, entry_date, entry_address, entry_classid, listbox):
    student_id = entry_id.get()
    name = entry_name.get()
    date = entry_date.get()
    address = entry_address.get()
    class_id = entry_classid.get()

    if not student_id or not name:
        messagebox.showwarning("Input Error", "Vui lòng nhập đầy đủ thông tin sinh viên")
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
            messagebox.showerror("Lỗi cơ sử dữ liệu", "Không thể thêm sinh viên vào trường dữ liệu: " + str(e))
        finally:
            cursor.close()
            connection.close()

# Hàm sửa sinh viên
def edit_student(listbox, entry_id, entry_name, entry_date, entry_address, entry_classid):
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
def delete_student(listbox):
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

def clear_entries(listbox, entry_id, entry_name, entry_date, entry_address, entry_classid):
    entry_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_date.delete(0, tk.END)
    entry_address.delete(0, tk.END)
    entry_classid.delete(0, tk.END)
