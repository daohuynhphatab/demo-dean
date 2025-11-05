from database import connect_to_db
import tkinter as tk
from tkinter import messagebox
def open_class_management():
 def add_class(entry_class_id, entry_class_name, entry_class_khoa, class_listbox):
    class_id = entry_class_id.get()
    class_name = entry_class_name.get()
    class_khoa = entry_class_khoa.get()
    
    if not class_id or not class_name or not class_khoa:
        messagebox.showwarning("Input Error", "Vui lòng nhập đầy đủ thông tin về lớp học")
        return

    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            sql = "INSERT INTO lop (malop, tenlop, makhoa) VALUES (%s, %s, %s)"
            cursor.execute(sql, (class_id, class_name, class_khoa))
            connection.commit()
            messagebox.showinfo("Success", f"Thêm lớp học {class_name} thành công")
            class_listbox.insert(tk.END, f"{class_id} - {class_name} - {class_khoa}")
            clear_class_entries(entry_class_id, entry_class_name, entry_class_khoa)
        except Exception as e:
            messagebox.showerror("Database Error", "Failed to add class: " + str(e))
        finally:
            cursor.close()
            connection.close()

 def edit_class(class_listbox, entry_class_id, entry_class_name, entry_class_khoa):
    selected = class_listbox.curselection()
    if not selected:
        messagebox.showwarning("Select Error", "Vui lòng chọn lớp học để sửa")
        return

    class_item = class_listbox.get(selected)
    class_id = class_item.split(" - ")[0]
    
    class_name = entry_class_name.get()
    class_khoa = entry_class_khoa.get()

    if not class_name or not class_khoa:
        messagebox.showwarning("Input Error", "Vui lòng nhập đầy đủ thông tin để sửa")
        return

    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            sql = "UPDATE lop SET tenlop = %s, makhoa = %s WHERE malop = %s"
            cursor.execute(sql, (class_name, class_khoa, class_id))
            connection.commit()
            messagebox.showinfo("Success", f"Sửa lớp học {class_id} thành công")
            class_listbox.delete(selected)
            class_listbox.insert(selected, f"{class_id} - {class_name} - {class_khoa}")
            clear_class_entries(entry_class_id, entry_class_name, entry_class_khoa)
        except Exception as e:
            messagebox.showerror("Database Error", "Failed to edit class: " + str(e))
        finally:
            cursor.close()
            connection.close()

 def delete_class(class_listbox):
    selected = class_listbox.curselection()
    if not selected:
        messagebox.showwarning("Select Error", "Vui lòng chọn lớp học để xóa")
        return

    class_item = class_listbox.get(selected)
    class_id = class_item.split(" - ")[0]

    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            sql = "DELETE FROM lop WHERE malop = %s"
            cursor.execute(sql, (class_id,))
            connection.commit()
            messagebox.showinfo("Success", f"Xóa lớp học {class_id} thành công")
            class_listbox.delete(selected)
        except Exception as e:
            messagebox.showerror("Database Error", "Failed to delete class: " + str(e))
        finally:
            cursor.close()
            connection.close()

def clear_class_entries(entry_class_id, entry_class_name, entry_class_khoa):
    entry_class_id.delete(0, tk.END)
    entry_class_name.delete(0, tk.END)
    entry_class_khoa.delete(0, tk.END)