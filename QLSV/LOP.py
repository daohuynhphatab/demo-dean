import customtkinter as ctk
from tkinter import messagebox, END


class ClassManagerFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # === Tiêu đề ===
        title = ctk.CTkLabel(self, text="Quản lý lớp học", font=ctk.CTkFont(size=20, weight="bold"))
        title.grid(row=0, column=0, columnspan=2, pady=10)

        # === Form nhập thông tin lớp ===
        form_frame = ctk.CTkFrame(self)
        form_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nw")

        ctk.CTkLabel(form_frame, text="Mã lớp:").grid(row=0, column=0, sticky="w", pady=2)
        ctk.CTkLabel(form_frame, text="Tên lớp:").grid(row=1, column=0, sticky="w", pady=2)
        ctk.CTkLabel(form_frame, text="Khoa:").grid(row=2, column=0, sticky="w", pady=2)
        ctk.CTkLabel(form_frame, text="Cố vấn học tập:").grid(row=3, column=0, sticky="w", pady=2)

        self.entry_id = ctk.CTkEntry(form_frame, width=200)
        self.entry_name = ctk.CTkEntry(form_frame, width=200)
        self.entry_faculty = ctk.CTkEntry(form_frame, width=200)
        self.entry_teacher = ctk.CTkEntry(form_frame, width=200)

        self.entry_id.grid(row=0, column=1, pady=2)
        self.entry_name.grid(row=1, column=1, pady=2)
        self.entry_faculty.grid(row=2, column=1, pady=2)
        self.entry_teacher.grid(row=3, column=1, pady=2)

        # === Nút chức năng ===
        btn_frame = ctk.CTkFrame(form_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)

        ctk.CTkButton(btn_frame, text="Thêm", command=self.add_class).grid(row=0, column=0, padx=5)
        ctk.CTkButton(btn_frame, text="Sửa", command=self.update_class).grid(row=0, column=1, padx=5)
        ctk.CTkButton(btn_frame, text="Xóa", command=self.delete_class).grid(row=0, column=2, padx=5)
        ctk.CTkButton(btn_frame, text="Xóa hết", fg_color="red", command=self.clear_all).grid(row=0, column=3, padx=5)

        # === Danh sách lớp ===
        list_frame = ctk.CTkFrame(self)
        list_frame.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")

        self.listbox = ctk.CTkTextbox(list_frame, width=450, height=350)
        self.listbox.grid(row=0, column=0, padx=10, pady=10)

        # Dữ liệu lớp (demo)
        self.classes = []

        self.listbox.bind("<ButtonRelease-1>", self.select_class)

    # === Các hàm xử lý ===
    def refresh_list(self):
        self.listbox.delete("1.0", END)
        for i, c in enumerate(self.classes, start=1):
            self.listbox.insert(
                END, f"{i}. {c['id']} - {c['name']} | {c['faculty']} | CVHT: {c['teacher']}\n"
            )

    def add_class(self):
        cid = self.entry_id.get().strip()
        name = self.entry_name.get().strip()
        faculty = self.entry_faculty.get().strip()
        teacher = self.entry_teacher.get().strip()

        if not cid or not name:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập Mã lớp và Tên lớp!")
            return

        self.classes.append({
            "id": cid,
            "name": name,
            "faculty": faculty,
            "teacher": teacher
        })
        self.refresh_list()
        self.clear_form()

    def select_class(self, event=None):
        try:
            index = int(self.listbox.index("insert").split('.')[0]) - 1
            c = self.classes[index]
            self.entry_id.delete(0, END)
            self.entry_name.delete(0, END)
            self.entry_faculty.delete(0, END)
            self.entry_teacher.delete(0, END)

            self.entry_id.insert(0, c["id"])
            self.entry_name.insert(0, c["name"])
            self.entry_faculty.insert(0, c["faculty"])
            self.entry_teacher.insert(0, c["teacher"])
        except:
            pass

    def update_class(self):
        cid = self.entry_id.get().strip()
        for c in self.classes:
            if c["id"] == cid:
                c["name"] = self.entry_name.get().strip()
                c["faculty"] = self.entry_faculty.get().strip()
                c["teacher"] = self.entry_teacher.get().strip()
                self.refresh_list()
                messagebox.showinfo("Thành công", "Đã cập nhật thông tin lớp!")
                return
        messagebox.showerror("Lỗi", "Không tìm thấy lớp để sửa!")

    def delete_class(self):
        cid = self.entry_id.get().strip()
        before = len(self.classes)
        self.classes = [c for c in self.classes if c["id"] != cid]
        after = len(self.classes)
        if before == after:
            messagebox.showerror("Lỗi", "Không tìm thấy lớp để xóa!")
        else:
            self.refresh_list()
            self.clear_form()
            messagebox.showinfo("Thành công", "Đã xóa lớp!")

    def clear_all(self):
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa toàn bộ danh sách lớp?"):
            self.classes.clear()
            self.refresh_list()
            self.clear_form()

    def clear_form(self):
        for entry in (self.entry_id, self.entry_name, self.entry_faculty, self.entry_teacher):
            entry.delete(0, END)
