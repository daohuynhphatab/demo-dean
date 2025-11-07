import customtkinter as ctk
from tkinter import messagebox, END
from database import get_connection


class StudentManagerFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # === Tiêu đề ===
        title = ctk.CTkLabel(self, text="Quản lý sinh viên", font=ctk.CTkFont(size=20, weight="bold"))
        title.grid(row=0, column=0, columnspan=2, pady=10)

        # === Form nhập thông tin ===
        form_frame = ctk.CTkFrame(self)
        form_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nw")

        ctk.CTkLabel(form_frame, text="Mã SV:").grid(row=0, column=0, sticky="w", pady=2)
        ctk.CTkLabel(form_frame, text="Họ tên:").grid(row=1, column=0, sticky="w", pady=2)
        ctk.CTkLabel(form_frame, text="Mã lớp:").grid(row=2, column=0, sticky="w", pady=2)
        ctk.CTkLabel(form_frame, text="Khoa:").grid(row=3, column=0, sticky="w", pady=2)

        self.entry_id = ctk.CTkEntry(form_frame, width=200)
        self.entry_name = ctk.CTkEntry(form_frame, width=200)
        self.entry_class = ctk.CTkEntry(form_frame, width=200)
        self.entry_faculty = ctk.CTkEntry(form_frame, width=200)

        self.entry_id.grid(row=0, column=1, pady=2)
        self.entry_name.grid(row=1, column=1, pady=2)
        self.entry_class.grid(row=2, column=1, pady=2)
        self.entry_faculty.grid(row=3, column=1, pady=2)

        # === Nút chức năng ===
        btn_frame = ctk.CTkFrame(form_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)

        ctk.CTkButton(btn_frame, text="Thêm", command=self.add_student).grid(row=0, column=0, padx=5)
        ctk.CTkButton(btn_frame, text="Sửa", command=self.update_student).grid(row=0, column=1, padx=5)
        ctk.CTkButton(btn_frame, text="Xóa", command=self.delete_student).grid(row=0, column=2, padx=5)
        ctk.CTkButton(btn_frame, text="Làm mới", fg_color="gray", command=self.load_students).grid(row=0, column=3, padx=5)

        # === Bảng hiển thị danh sách sinh viên ===
        list_frame = ctk.CTkFrame(self)
        list_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        self.listbox = ctk.CTkTextbox(list_frame, width=600, height=350)
        self.listbox.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

        # Khi chọn dòng trong listbox
        self.listbox.bind("<ButtonRelease-1>", self.select_student)

        # Tải dữ liệu ban đầu
        self.load_students()

    # === Tải danh sách sinh viên ===
    def load_students(self):
        conn = get_connection()
        if not conn:
            return

        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM sinhvien")
        self.students = cursor.fetchall()
        conn.close()

        self.refresh_list()

    # === Cập nhật listbox ===
    def refresh_list(self):
        self.listbox.delete("1.0", END)
        for i, sv in enumerate(self.students, start=1):
            self.listbox.insert(END, f"{i}. {sv['id']} - {sv['name']} | {sv['classid']} | {sv['faculty']}\n")

    # === Thêm sinh viên ===
    def add_student(self):
        sid = self.entry_id.get().strip()
        name = self.entry_name.get().strip()
        sclass = self.entry_class.get().strip()
        faculty = self.entry_faculty.get().strip()

        if not sid or not name or not sclass or not faculty:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin!")
            return

        conn = get_connection()
        if not conn:
            return

        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO sinhvien (id, name, classid, faculty) VALUES (%s, %s, %s, %s)",
                (sid, name, sclass, faculty)
            )
            conn.commit()
            messagebox.showinfo("Thành công", "Đã thêm sinh viên!")
            self.load_students()
            self.clear_form()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể thêm sinh viên: {e}")
        finally:
            conn.close()

    # === Cập nhật sinh viên ===
    def update_student(self):
        sid = self.entry_id.get().strip()
        name = self.entry_name.get().strip()
        sclass = self.entry_class.get().strip()
        faculty = self.entry_faculty.get().strip()

        if not sid:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng chọn sinh viên cần sửa!")
            return

        conn = get_connection()
        if not conn:
            return

        cursor = conn.cursor()
        cursor.execute("SELECT id FROM sinhvien WHERE id=%s", (sid,))
        if not cursor.fetchone():
            messagebox.showerror("Lỗi", "Không tìm thấy sinh viên này!")
            conn.close()
            return

        try:
            cursor.execute(
                "UPDATE sinhvien SET name=%s, classid=%s, faculty=%s WHERE id=%s",
                (name, sclass, faculty, sid)
            )
            conn.commit()
            messagebox.showinfo("Thành công", "Đã cập nhật sinh viên!")
            self.load_students()
            self.clear_form()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể cập nhật: {e}")
        finally:
            conn.close()

    # === Xóa sinh viên ===
    def delete_student(self):
        sid = self.entry_id.get().strip()
        if not sid:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng chọn sinh viên cần xóa!")
            return

        if not messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa sinh viên {sid}?"):
            return

        conn = get_connection()
        if not conn:
            return

        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM sinhvien WHERE id=%s", (sid,))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã xóa sinh viên!")
            self.load_students()
            self.clear_form()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xóa sinh viên: {e}")
        finally:
            conn.close()

    # === Khi click chọn sinh viên trong list ===
    def select_student(self, event=None):
        try:
            line = self.listbox.get("insert linestart", "insert lineend")
            sid = line.split(".")[1].split("-")[0].strip()
            sv = next((s for s in self.students if s["id"] == sid), None)
            if sv:
                self.entry_id.delete(0, END)
                self.entry_name.delete(0, END)
                self.entry_class.delete(0, END)
                self.entry_faculty.delete(0, END)
                self.entry_id.insert(0, sv["id"])
                self.entry_name.insert(0, sv["name"])
                self.entry_class.insert(0, sv["classid"])
                self.entry_faculty.insert(0, sv["faculty"])
        except Exception:
            pass

    def clear_form(self):
        for entry in (self.entry_id, self.entry_name, self.entry_class, self.entry_faculty):
            entry.delete(0, END)
