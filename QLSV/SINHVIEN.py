import customtkinter as ctk
from tkinter import messagebox, END


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
        ctk.CTkLabel(form_frame, text="Lớp:").grid(row=2, column=0, sticky="w", pady=2)
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
        ctk.CTkButton(btn_frame, text="Xóa hết", fg_color="red", command=self.clear_all).grid(row=0, column=3, padx=5)

        # === Bảng hiển thị danh sách sinh viên ===
        list_frame = ctk.CTkFrame(self)
        list_frame.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")

        self.listbox = ctk.CTkTextbox(list_frame, width=450, height=350)
        self.listbox.grid(row=0, column=0, padx=10, pady=10)

        # Dữ liệu sinh viên (demo, có thể thay bằng database sau)
        self.students = []

        # Khi chọn dòng trong listbox
        self.listbox.bind("<ButtonRelease-1>", self.select_student)

    # === Hàm xử lý ===
    def refresh_list(self):
        self.listbox.delete("1.0", END)
        for i, sv in enumerate(self.students, start=1):
            self.listbox.insert(END, f"{i}. {sv['id']} - {sv['name']} | {sv['class']} | {sv['faculty']}\n")

    def add_student(self):
        sid = self.entry_id.get().strip()
        name = self.entry_name.get().strip()
        sclass = self.entry_class.get().strip()
        faculty = self.entry_faculty.get().strip()

        if not sid or not name:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập Mã SV và Họ tên!")
            return

        self.students.append({
            "id": sid,
            "name": name,
            "class": sclass,
            "faculty": faculty
        })
        self.refresh_list()
        self.clear_form()

    def select_student(self, event=None):
        try:
            index = int(self.listbox.index("insert").split('.')[0]) - 1
            sv = self.students[index]
            self.entry_id.delete(0, END)
            self.entry_name.delete(0, END)
            self.entry_class.delete(0, END)
            self.entry_faculty.delete(0, END)

            self.entry_id.insert(0, sv["id"])
            self.entry_name.insert(0, sv["name"])
            self.entry_class.insert(0, sv["class"])
            self.entry_faculty.insert(0, sv["faculty"])
        except:
            pass

    def update_student(self):
        sid = self.entry_id.get().strip()
        name = self.entry_name.get().strip()
        sclass = self.entry_class.get().strip()
        faculty = self.entry_faculty.get().strip()

        for sv in self.students:
            if sv["id"] == sid:
                sv["name"] = name
                sv["class"] = sclass
                sv["faculty"] = faculty
                self.refresh_list()
                messagebox.showinfo("Thành công", "Cập nhật sinh viên thành công!")
                return
        messagebox.showerror("Lỗi", "Không tìm thấy sinh viên để sửa!")

    def delete_student(self):
        sid = self.entry_id.get().strip()
        before = len(self.students)
        self.students = [sv for sv in self.students if sv["id"] != sid]
        after = len(self.students)

        if before == after:
            messagebox.showerror("Lỗi", "Không tìm thấy sinh viên để xóa!")
        else:
            self.refresh_list()
            self.clear_form()
            messagebox.showinfo("Thành công", "Đã xóa sinh viên!")

    def clear_all(self):
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa toàn bộ danh sách?"):
            self.students.clear()
            self.refresh_list()
            self.clear_form()

    def clear_form(self):
        for entry in (self.entry_id, self.entry_name, self.entry_class, self.entry_faculty):
            entry.delete(0, END)
