from database import connect_to_db
import tkinter as tk
from tkinter import messagebox

def open_department_management():

 def add_department(entry_department_id, entry_department_name, department_listbox):
    department_id = entry_department_id.get()
    department_name = entry_department_name.get()
    
    if not department_id or not department_name:
        messagebox.showwarning("Input Error", "Vui lòng nhập đầy đủ thông tin về khoa")
        return

    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            sql = "INSERT INTO khoa (makhoa, tenkhoa) VALUES (%s, %s)"
            cursor.execute(sql, (department_id, department_name))
            connection.commit()
            messagebox.showinfo("Success", f"Thêm khoa {department_name} thành công")
            department_listbox.insert(tk.END, f"{department_id} - {department_name}")
            clear_department_entries(entry_department_id, entry_department_name)
        except Exception as e:
            messagebox.showerror("Database Error", "Failed to add department: " + str(e))
        finally:
            cursor.close()
            connection.close()

 def edit_department(department_listbox, entry_department_id, entry_department_name):
    selected = department_listbox.curselection()
    if not selected:
        messagebox.showwarning("Select Error", "Vui lòng chọn khoa để sửa")
        return

    department_item = department_listbox.get(selected)
    department_id = department_item.split(" - ")[0]
    
    department_name = entry_department_name.get()

    if not department_name:
        messagebox.showwarning("Input Error", "Vui lòng nhập tên khoa để sửa")
        return

    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            sql = "UPDATE khoa SET tentkhoa = %s WHERE makhoa = %s"
            cursor.execute(sql, (department_name, department_id))
            connection.commit()
            messagebox.showinfo("Success", f"Sửa khoa {department_id} thành công")
            department_listbox.delete(selected)
            department_listbox.insert(selected, f"{department_id} - {department_name}")
            clear_department_entries(entry_department_id, entry_department_name)
        except Exception as e:
            messagebox.showerror("Database Error", "Failed to edit department: " + str(e))
        finally:
            cursor.close()
            connection.close()

 def delete_department(department_listbox):
    selected = department_listbox.curselection()
    if not selected:
        messagebox.showwarning("Select Error", "Vui lòng chọn khoa để xóa")
        return

    department_item = department_listbox.get(selected)
    department_id = department_item.split(" - ")[0]

    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            sql = "DELETE FROM khoa WHERE makhoa = %s"
            cursor.execute(sql, (department_id,))
            connection.commit()
            messagebox.showinfo("Success", f"Xóa khoa {department_id} thành công")
            department_listbox.delete(selected)
        except Exception as e:
            messagebox.showerror("Database Error", "Failed to delete department: " + str(e))
        finally:
            cursor.close()
            connection.close()

 def clear_department_entries(entry_department_id, entry_department_name):
    entry_department_id.delete(0, tk.END)
    entry_department_name.delete(0, tk.END)