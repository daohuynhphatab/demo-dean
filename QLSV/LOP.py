import customtkinter as ctk
from tkinter import messagebox, END
from database import get_connection  


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
        ctk.CTkButton(btn_frame, text="Tải lại", command=self.load_classes).grid(row=0, column=4, padx=5)

        # === Danh sách lớp ===
        list_frame = ctk.CTkFrame(self)
        list_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        self.listbox = ctk.CTkTextbox(list_frame, width=600, height=350)
        self.listbox.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

        # Cache dữ liệu lớp
        self.classes = []

        self.listbox.bind("<ButtonRelease-1>", self.select_class)

        # Tải dữ liệu ban đầu
        self.load_classes()

    # ---------------- DB: load ----------------
    def load_classes(self):
        """Tải danh sách lớp từ DB vào cache self.classes rồi refresh GUI."""
        conn = get_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT malop, tenlop, makhoa, cvht FROM lop ORDER BY malop")
            rows = cursor.fetchall()
            self.classes = rows
            cursor.close()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tải danh sách lớp:\n{e}")
            self.classes = []
        finally:
            try:
                conn.close()
            except:
                pass

        self.refresh_list()

    def refresh_list(self):
        """Hiển thị cache self.classes lên textbox."""
        self.listbox.delete("1.0", END)
        for i, c in enumerate(self.classes, start=1):
            teacher = c.get("cvht", "") if isinstance(c, dict) else ""
            self.listbox.insert(
                END, f"{i}. {c['malop']} - {c['tenlop']} | {c['makhoa']} | CVHT: {teacher}\n"
            )

    # ---------------- CRUD: Add ----------------
    def add_class(self):
        cid = self.entry_id.get().strip()
        name = self.entry_name.get().strip()
        faculty = self.entry_faculty.get().strip()
        teacher = self.entry_teacher.get().strip()

        if not cid or not name:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập Mã lớp và Tên lớp!")
            return

        conn = get_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            sql = "INSERT INTO lop (malop, tenlop, makhoa, cvht) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (cid, name, faculty, teacher))
            conn.commit()
            cursor.close()

            # cập nhật cache và giao diện
            rec = {"malop": cid, "tenlop": name, "makhoa": faculty, "cvht": teacher}
            self.classes.append(rec)
            self.refresh_list()
            self.clear_form()
            messagebox.showinfo("Thành công", "Đã thêm lớp vào database.")
        except Exception as e:
            messagebox.showerror("Lỗi thêm", f"Không thể thêm lớp:\n{e}")
        finally:
            try:
                conn.close()
            except:
                pass

    # ---------------- CRUD: Update ----------------
    def update_class(self):
        cid = self.entry_id.get().strip()
        if not cid:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng chọn lớp cần sửa!")
            return

        name = self.entry_name.get().strip()
        faculty = self.entry_faculty.get().strip()
        teacher = self.entry_teacher.get().strip()

        conn = get_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            sql = "UPDATE lop SET tenlop=%s, makhoa=%s, cvht=%s WHERE malop=%s"
            cursor.execute(sql, (name, faculty, teacher, cid))
            if cursor.rowcount == 0:
                messagebox.showerror("Lỗi", "Không tìm thấy lớp để cập nhật.")
            else:
                conn.commit()
                # cập nhật cache
                for c in self.classes:
                    if c.get("malop") == cid:
                        c["tenlop"] = name
                        c["makhoa"] = faculty
                        c["cvht"] = teacher
                        break
                self.refresh_list()
                self.clear_form()
                messagebox.showinfo("Thành công", "Đã cập nhật lớp.")
            cursor.close()
        except Exception as e:
            messagebox.showerror("Lỗi cập nhật", f"Không thể cập nhật lớp:\n{e}")
        finally:
            try:
                conn.close()
            except:
                pass

    # ---------------- CRUD: Delete ----------------
    def delete_class(self):
        cid = self.entry_id.get().strip()
        if not cid:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng chọn lớp cần xóa!")
            return

        if not messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa lớp {cid}?"):
            return

        conn = get_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            sql = "DELETE FROM lop WHERE malop=%s"
            cursor.execute(sql, (cid,))
            if cursor.rowcount == 0:
                messagebox.showerror("Lỗi", "Không tìm thấy lớp để xóa.")
            else:
                conn.commit()
                # cập nhật cache và giao diện
                self.classes = [c for c in self.classes if c.get("malop") != cid]
                self.refresh_list()
                self.clear_form()
                messagebox.showinfo("Thành công", "Đã xóa lớp.")
            cursor.close()
        except Exception as e:
            messagebox.showerror("Lỗi xóa", f"Không thể xóa lớp:\n{e}")
        finally:
            try:
                conn.close()
            except:
                pass

    # ---------------- CRUD: Clear all ----------------
    def clear_all(self):
        if not messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa toàn bộ danh sách lớp trong database?"):
            return

        conn = get_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM lop")
            conn.commit()
            cursor.close()
            self.classes.clear()
            self.refresh_list()
            self.clear_form()
            messagebox.showinfo("Thành công", "Đã xóa toàn bộ danh sách lớp.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xóa toàn bộ:\n{e}")
        finally:
            try:
                conn.close()
            except:
                pass

    # ---------------- Chọn dòng ----------------
    def select_class(self, event=None):
        try:
            line = self.listbox.get("insert linestart", "insert lineend")
            parts = line.split(".")
            if len(parts) < 2:
                return
            right = parts[1].strip()
            malop = right.split("-")[0].strip()
            rec = next((c for c in self.classes if c.get("malop") == malop), None)
            if rec:
                self.entry_id.delete(0, END); self.entry_id.insert(0, rec.get("malop", ""))
                self.entry_name.delete(0, END); self.entry_name.insert(0, rec.get("tenlop", ""))
                self.entry_faculty.delete(0, END); self.entry_faculty.insert(0, rec.get("makhoa", ""))
                self.entry_teacher.delete(0, END); self.entry_teacher.insert(0, rec.get("cvht", ""))
        except Exception:
            pass

    def clear_form(self):
        for entry in (self.entry_id, self.entry_name, self.entry_faculty, self.entry_teacher):
            entry.delete(0, END)
