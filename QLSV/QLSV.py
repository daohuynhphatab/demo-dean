from pyclbr import Class
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

# KHOA
def add_department():
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
            values = (department_id, department_name)
            cursor.execute(sql, values)
            connection.commit()
            messagebox.showinfo("Success", f"Thêm khoa {department_name} thành công")
            department_listbox.insert(tk.END, f"{department_id} - {department_name}")
            clear_department_entries()
        except Exception as e:
            messagebox.showerror("Database Error", "Failed to add department: " + str(e))
        finally:
            cursor.close()
            connection.close()

# Hàm sửa khoa
def edit_department():
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
            sql = "UPDATE khoa SET tenkhoa = %s WHERE makhoa = %s"
            values = (department_name, department_id)
            cursor.execute(sql, values)
            connection.commit()
            messagebox.showinfo("Success", f"Sửa khoa {department_id} thành công")
            department_listbox.delete(selected)
            department_listbox.insert(selected, f"{department_id} - {department_name}")
            clear_department_entries()
        except Exception as e:
            messagebox.showerror("Database Error", "Failed to edit department: " + str(e))
        finally:
            cursor.close()
            connection.close()

# Hàm xóa khoa
def delete_department():
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

def clear_department_entries():
    entry_department_id.delete(0, tk.END)
    entry_department_name.delete(0, tk.END)

# Giao diện quản lý khoa
def open_department_management():
    global department_listbox, entry_department_id, entry_department_name

    department_window = tk.Toplevel(root)
    department_window.title("Quản Lý Khoa")

    # Tiêu đề
    Label(department_window, text="Quản Lý Khoa", font=("Arial", 20)).grid(row=0, columnspan=2, pady=10)

    # Danh sách khoa
    department_listbox = Listbox(department_window, width=80, height=10)
    department_listbox.grid(row=1, columnspan=2)

    # Trường nhập Mã khoa
    Label(department_window, text="Mã khoa:").grid(row=2, column=0, sticky=W, padx=10)
    entry_department_id = Entry(department_window, width=30)
    entry_department_id.grid(row=2, column=1, sticky=W)

    # Trường nhập Tên khoa
    Label(department_window, text="Tên khoa:").grid(row=3, column=0, sticky=W, padx=10)
    entry_department_name = Entry(department_window, width=30)
    entry_department_name.grid(row=3, column=1, sticky=W)

    # Nút thêm khoa
    Button(department_window, text="Thêm Khoa", command=add_department, width=15).grid(row=4, columnspan=2, pady=10)

    # Nút xóa khoa
    Button(department_window, text="Xóa Khoa", command=delete_department, width=15).grid(row=5, columnspan=2, pady=10)

    # Nút sửa khoa
    Button(department_window, text="Sửa Khoa", command=edit_department, width=15).grid(row=6, columnspan=2, pady=10)

    # Nút thoát
    Button(department_window, text="Thoát Khoa", command=department_window.destroy, width=15).grid(row=7, columnspan=2, pady=10)



def clear_class_entries():
    entry_class_id.delete(0, tk.END)
    entry_class_name.delete(0, tk.END)
    entry_class_khoa.delete(0, tk.END)

def add_class():
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
            values = (class_id, class_name, class_khoa)
            cursor.execute(sql, values)
            connection.commit()
            messagebox.showinfo("Success", f"Thêm lớp học {class_name} thành công")
            class_listbox.insert(tk.END, f"{class_id} - {class_name} - {class_khoa}")
            clear_class_entries()
        except Exception as e:
            messagebox.showerror("Database Error", "Failed to add subject: " + str(e))
        finally:
            cursor.close()
            connection.close()

def delete_class():
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
            messagebox.showerror("Database Error", "Failed to delete subject: " + str(e))
        finally:
            cursor.close()
            connection.close()

def edit_class():
    selected = class_listbox.curselection()
    if not selected:
        messagebox.showwarning("Select Error", "Vui lòng chọn lớp học để sửa")
        return

    class_item = class_listbox.get(selected)
    class_id = class_item.split(" - ")[0]
    
    # Lấy thông tin để sửa
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
            values = (class_name, class_khoa, class_id)
            cursor.execute(sql, values)
            connection.commit()
            messagebox.showinfo("Success", f"Sửa lớp học {class_id} thành công")
            class_listbox.delete(selected)
            class_listbox.insert(selected, f"{class_id} - {class_name} - {class_khoa}")
            clear_class_entries()
        except Exception as e:
            messagebox.showerror("Database Error", "Failed to edit subject: " + str(e))
        finally:
            cursor.close()
            connection.close()

# Giao diện lớp học
def open_class_management():
    global class_listbox, entry_class_id, entry_class_name, entry_class_khoa

    class_window = tk.Toplevel(root)
    class_window.title("Quản Lý Lớp Học")

    # Tiêu đề
    Label(class_window, text="Quản Lý Lớp Học", font=("Arial", 20)).grid(row=0, columnspan=2, pady=10)

    # Danh sách lớp học
    class_listbox = Listbox(class_window, width=80, height=10)
    class_listbox.grid(row=1, columnspan=2)

    # Trường nhập Mã lớp học
    Label(class_window, text="Mã lớp học:").grid(row=2, column=0, sticky=tk.W, padx=10)
    entry_class_id = Entry(class_window, width=30)
    entry_class_id.grid(row=2, column=1, sticky=tk.W)

    # Trường nhập Tên lớp học
    Label(class_window, text="Tên lớp học:").grid(row=3, column=0, sticky=tk.W, padx=10)
    entry_class_name = Entry(class_window, width=30)
    entry_class_name.grid(row=3, column=1, sticky=tk.W)

    # Trường nhập mã khoa
    Label(class_window, text="Mã khoa:").grid(row=4, column=0, sticky=tk.W, padx=10)
    entry_class_khoa = Entry(class_window, width=30)
    entry_class_khoa.grid(row=4, column=1, sticky=tk.W)

    # Nút thêm lớp học
    Button(class_window, text="Thêm Lớp Học", command=add_class, width=15).grid(row=5, columnspan=2, pady=10)

    # Nút xóa lớp học
    Button(class_window, text="Xóa Lớp Học", command=delete_class, width=15).grid(row=6, columnspan=2, pady=10)

    # Nút sửa lớp học
    Button(class_window, text="Sửa Lớp Học", command=edit_class, width=15).grid(row=7, columnspan=2, pady=10)

    # Nút thoát
    Button(class_window, text="Thoát Lớp Học", command=class_window.destroy, width=15).grid(row=8, columnspan=2, pady=10)

#Giao diện đăng kí môn học

# Hàm thêm môn học đăng ký
def add_subject_enrollment():
    student_id = entry_student_id.get()
    course_id = entry_course_id.get()
    semester = entry_semester.get()

    if not student_id or not course_id or not semester:
        messagebox.showwarning("Input Error", "Vui lòng nhập đầy đủ thông tin đăng ký môn học")
        return

    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            sql = "INSERT INTO dangkimonhoc (masosv, mamonhoc, hocki) VALUES (%s, %s, %s)"
            values = (student_id, course_id, semester)
            cursor.execute(sql, values)
            connection.commit()
            messagebox.showinfo("Success", "Đăng ký môn học thành công!")
            subject_listbox.insert(tk.END, f"{student_id} - {course_id} - {semester}")
            clear_subject_entries()
        except Exception as e:
            messagebox.showerror("Database Error", "Không thể đăng ký môn học: " + str(e))
        finally:
            cursor.close()
            connection.close()

def clear_subject_entries():
    entry_student_id.delete(0, tk.END)
    entry_course_id.delete(0, tk.END)
    entry_semester.delete(0, tk.END)

# Giao diện quản lý đăng ký môn học
def open_subject_enrollment_management():
    global subject_listbox, entry_student_id, entry_course_id, entry_semester

    subject_enrollment_window = tk.Toplevel(root)
    subject_enrollment_window.title("Đăng Ký Môn Học")

    # Tiêu đề
    Label(subject_enrollment_window, text="Quản Lý Đăng Ký Môn Học", font=("Arial", 20)).grid(row=0, columnspan=2, pady=10)

    # Danh sách đăng ký môn học
    subject_listbox = Listbox(subject_enrollment_window, width=80, height=10)
    subject_listbox.grid(row=1, columnspan=2)

    # Trường nhập Mã sinh viên
    Label(subject_enrollment_window, text="Mã sinh viên:").grid(row=2, column=0, sticky=W, padx=10)
    entry_student_id = Entry(subject_enrollment_window, width=30)
    entry_student_id.grid(row=2, column=1, sticky=W)

    # Trường nhập Mã môn học
    Label(subject_enrollment_window, text="Mã môn học:").grid(row=3, column=0, sticky=W, padx=10)
    entry_course_id = Entry(subject_enrollment_window, width=30)
    entry_course_id.grid(row=3, column=1, sticky=W)

    # Trường nhập Học kỳ
    Label(subject_enrollment_window, text="Học kỳ:").grid(row=4, column=0, sticky=W, padx=10)
    entry_semester = Entry(subject_enrollment_window, width=30)
    entry_semester.grid(row=4, column=1, sticky=W)

    # Nút thêm đăng ký môn học
    Button(subject_enrollment_window, text="Đăng Ký", command=add_subject_enrollment, width=15, bg='lightgreen').grid(row=5, columnspan=2, pady=10)

    # Nút thoát
    Button(subject_enrollment_window, text="Thoát", command=subject_enrollment_window.destroy, width=15, bg='lightcoral').grid(row=6, columnspan=2, pady=10)


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

    # Hàm chỉnh sửa môn học
    def edit_subject():
        selected_subject = subject_listbox.curselection()
        if not selected_subject:
            messagebox.showwarning("Selection Error", "Vui lòng chọn môn học để sửa")
            return

        subject_info = subject_listbox.get(selected_subject)
        subject_id = subject_info.split(" - ")[0]
        subject_name = entry_subject_name.get()
        subject_TC = entry_subject_TC.get()

        if not subject_name:
            messagebox.showwarning("Input Error", "Vui lòng nhập tên môn học")
            return

        connection = connect_to_db()
        if connection:
            try:
                cursor = connection.cursor()
                sql = "UPDATE monhoc SET name=%s, tc=%s WHERE id=%s"
                values = (subject_name, subject_TC, subject_id)
                cursor.execute(sql, values)
                connection.commit()
                messagebox.showinfo("Success", f"Sửa môn học {subject_id} thành công")
                subject_listbox.delete(selected_subject)
                subject_listbox.insert(selected_subject, f"{subject_id} - {subject_name} - {subject_TC}")
            except Exception as e:
                messagebox.showerror("Database Error", "Failed to edit subject: " + str(e))
            finally:
                cursor.close()
                connection.close()

    # Hàm xóa môn học
    def delete_subject():
        selected_subject = subject_listbox.curselection()
        if not selected_subject:
            messagebox.showwarning("Selection Error", "Vui lòng chọn môn học để xóa")
            return

        subject_info = subject_listbox.get(selected_subject)
        subject_id = subject_info.split(" - ")[0]

        connection = connect_to_db()
        if connection:
            try:
                cursor = connection.cursor()
                sql = "DELETE FROM monhoc WHERE id = %s"
                cursor.execute(sql, (subject_id,))
                connection.commit()
                messagebox.showinfo("Success", f"Đã xóa môn học có mã {subject_id}")
                subject_listbox.delete(selected_subject)
            except Exception as e:
                messagebox.showerror("Database Error", "Failed to delete subject: " + str(e))
            finally:
                cursor.close()
                connection.close()

    # Hàm tìm kiếm môn học
    def search_subject():
        subject_id = entry_subject_id.get()
        if not subject_id:
            messagebox.showwarning("Input Error", "Vui lòng nhập mã môn học để tìm kiếm")
            return

        connection = connect_to_db()
        if connection:
            try:
                cursor = connection.cursor()
                sql = "SELECT * FROM monhoc WHERE id = %s"
                cursor.execute(sql, (subject_id,))
                result = cursor.fetchone()
                if result:
                    # Hiển thị kết quả tìm kiếm
                    entry_subject_name.delete(0, tk.END)
                    entry_subject_name.insert(0, result[1])  # Tên môn
                    entry_subject_TC.delete(0, tk.END)
                    entry_subject_TC.insert(0, result[2])  # Số tín chỉ
                else:
                    messagebox.showinfo("Search Result", "Không tìm thấy môn học với mã này")
            except Exception as e:
                messagebox.showerror("Database Error", "Failed to search subject: " + str(e))
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
    # Nút sửa môn học
    Button(subject_window, text="Sửa Môn Học", command=edit_subject, width=15).grid(row=6, columnspan=2, pady=10)
    # Nút tìm kiếm môn học
    Button(subject_window, text="Tìm Môn Học", command=search_subject, width=15).grid(row=7, columnspan=2, pady=10)
    # Nút thoát
    Button(subject_window, text="Thoát Môn Học", command=subject_window.destroy, width=15).grid(row=8, columnspan=2, pady=10)

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

# Nút Lớp học
Button(frame_btn, text="Lớp học", command=open_class_management, width=10).pack(side='left', padx=5)

# Nút Khoa
Button(frame_btn, text="Khoa", command=open_department_management, width=10).pack(side='left', padx=5)

# Nút Đăng ký môn học
Button(frame_btn, text="Đăng ký môn học", command=open_subject_enrollment_management, width=15).pack(side='left', padx=5)

# Nút thoát
Button(frame_btn, text="Thoát", command=root.quit, width=10).pack(side='left', padx=5)

# Chạy ứng dụng
root.mainloop()