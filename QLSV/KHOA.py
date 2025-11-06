import customtkinter as ctk
from tkinter import messagebox, END


class FacultyManagerFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # === Tiêu đề ===
        title = ctk.CTkLabel(self, text="Quản lý khoa", font=ctk.CTkFont(size=20, weight="bold"))
        title.grid(row=0, column=0, columnspan=2, pady=10)

        # === Form nhập thông tin khoa ===
        form_frame = ctk.CTkFrame(self)
        form_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nw")

        ctk.CTkLabel(form_frame, text="Mã khoa:").grid(row=0, column=0, sticky="w", pady=2)
        ctk.CTkLabel(form_frame, text="Tên khoa:").grid(row=1, column=0, sticky="w", pady=2)
        ctk.CTkLabel(form_frame, text="Trưởng khoa:").grid(row=2, column=0, sticky="w", pady=2)
        ctk.CTkLabel(form_frame, text="Số điện thoại:").grid(row=3, column=0, sticky="w", pady=2)

        self.entry_id = ctk.CTkEntry(form_frame, width=200)
        self.entry_name = ctk.CTkEntry(form_frame, width=200)
        self.entry_head = ctk.CTkEntry(form_frame, width=200)
        self.entry_phone = ctk.CTkEntry(form_frame, width=200)

        self.entry_id.grid(row=0, column=1, pady=2)
        self.entry_name.grid(row=1, column=1, pady=2)
        self.entry_head.grid(row=2, column=1, pady=2)
        self.entry_phone.grid(row=3, column=1, pady=2)

        # === Nút chức năng ===
        btn_frame = ctk.CTkFrame(form_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)

        ctk.CTkButton(btn_frame, text="Thêm", command=self.add_faculty).grid(row=0, column=0, padx=5)
        ctk.CTkButton(btn_frame, text="Sửa", command=self.update_faculty).grid(row=0, column=1, padx=5)
        ctk.CTkButton(btn_frame, text="Xóa", command=self.delete_faculty).grid(row=0, column=2, padx=5)
        ctk.CTkButton(btn_frame, text="Xóa hết", fg_color="red", command=self.clear_all).grid(row=0, column=3, padx=5)

        # === Danh sách khoa ===
        list_frame = ctk.CTkFrame(self)
        list_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        self.listbox = ctk.CTkTextbox(list_frame, width=600, height=350)
        self.listbox.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

        # Dữ liệu khoa (demo)
        self.faculties = []

        self.listbox.bind("<ButtonRelease-1>", self.select_faculty)

    # === Các hàm xử lý ===
    def refresh_list(self):
        self.listbox.delete("1.0", END)
        for i, f in enumerate(self.faculties, start=1):
            self.listbox.insert(
                END,
                f"{i}. {f['id']} - {f['name']} | Trưởng khoa: {f['head']} | ĐT: {f['phone']}\n"
            )

    def add_faculty(self):
        fid = self.entry_id.get().strip()
        name = self.entry_name.get().strip()
        head = self.entry_head.get().strip()
        phone = self.entry_phone.get().strip()

        if not fid or not name:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập Mã khoa và Tên khoa!")
            return

        self.faculties.append({
            "id": fid,
            "name": name,
            "head": head,
            "phone": phone
        })
        self.refresh_list()
        self.clear_form()

    def select_faculty(self, event=None):
        try:
            index = int(self.listbox.index("insert").split('.')[0]) - 1
            f = self.faculties[index]
            self.entry_id.delete(0, END)
            self.entry_name.delete(0, END)
            self.entry_head.delete(0, END)
            self.entry_phone.delete(0, END)

            self.entry_id.insert(0, f["id"])
            self.entry_name.insert(0, f["name"])
            self.entry_head.insert(0, f["head"])
            self.entry_phone.insert(0, f["phone"])
        except:
            pass

    def update_faculty(self):
        fid = self.entry_id.get().strip()
        for f in self.faculties:
            if f["id"] == fid:
                f["name"] = self.entry_name.get().strip()
                f["head"] = self.entry_head.get().strip()
                f["phone"] = self.entry_phone.get().strip()
                self.refresh_list()
                messagebox.showinfo("Thành công", "Đã cập nhật thông tin khoa!")
                return
        messagebox.showerror("Lỗi", "Không tìm thấy khoa để sửa!")

    def delete_faculty(self):
        fid = self.entry_id.get().strip()
        before = len(self.faculties)
        self.faculties = [f for f in self.faculties if f["id"] != fid]
        after = len(self.faculties)
        if before == after:
            messagebox.showerror("Lỗi", "Không tìm thấy khoa để xóa!")
        else:
            self.refresh_list()
            self.clear_form()
            messagebox.showinfo("Thành công", "Đã xóa khoa!")

    def clear_all(self):
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa toàn bộ danh sách khoa?"):
            self.faculties.clear()
            self.refresh_list()
            self.clear_form()

    def clear_form(self):
        for entry in (self.entry_id, self.entry_name, self.entry_head, self.entry_phone):
            entry.delete(0, END)
