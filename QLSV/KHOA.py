import customtkinter as ctk
from tkinter import messagebox, END
from database import get_connection  # đảm bảo database.py có get_connection()


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
        ctk.CTkButton(btn_frame, text="Tải lại", command=self.load_faculties).grid(row=0, column=4, padx=5)

        # === Danh sách khoa ===
        list_frame = ctk.CTkFrame(self)
        list_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        self.listbox = ctk.CTkTextbox(list_frame, width=600, height=350)
        self.listbox.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

        # Dữ liệu khoa (cache từ DB)
        self.faculties = []

        self.listbox.bind("<ButtonRelease-1>", self.select_faculty)

        # Tải dữ liệu ban đầu từ DB
        self.load_faculties()

    # ---------------- DB liên quan ----------------
    def load_faculties(self):
        """Load danh sách khoa từ bảng 'khoa' (makhoa, tenkhoa, truongkhoa, sdt)."""
        conn = get_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT makhoa, tenkhoa, truongkhoa, sdt FROM khoa ORDER BY makhoa")
            rows = cursor.fetchall()
            self.faculties = rows
            cursor.close()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tải danh sách khoa:\n{e}")
            self.faculties = []
        finally:
            try:
                conn.close()
            except:
                pass

        self.refresh_list()

    def refresh_list(self):
        """Hiển thị cache self.faculties vào listbox."""
        self.listbox.delete("1.0", END)
        for i, f in enumerate(self.faculties, start=1):
            self.listbox.insert(
                END,
                f"{i}. {f['makhoa']} - {f['tenkhoa']} | Trưởng khoa: {f['truongkhoa']} | ĐT: {f['sdt']}\n"
            )

    # ---------------- CRUD (DB) ----------------
    def add_faculty(self):
        fid = self.entry_id.get().strip()
        name = self.entry_name.get().strip()
        head = self.entry_head.get().strip()
        phone = self.entry_phone.get().strip()

        if not fid or not name:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập Mã khoa và Tên khoa!")
            return

        conn = get_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            sql = "INSERT INTO khoa (makhoa, tenkhoa, truongkhoa, sdt) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (fid, name, head, phone))
            conn.commit()
            cursor.close()

            # cập nhật cache
            rec = {"makhoa": fid, "tenkhoa": name, "truongkhoa": head, "sdt": phone}
            self.faculties.append(rec)

            self.refresh_list()
            self.clear_form()
            messagebox.showinfo("Thành công", "Đã thêm khoa vào database.")
        except Exception as e:
            messagebox.showerror("Lỗi thêm", f"Không thể thêm khoa:\n{e}")
        finally:
            try:
                conn.close()
            except:
                pass

    def update_faculty(self):
        fid = self.entry_id.get().strip()
        if not fid:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng chọn khoa cần sửa!")
            return

        name = self.entry_name.get().strip()
        head = self.entry_head.get().strip()
        phone = self.entry_phone.get().strip()

        conn = get_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            sql = "UPDATE khoa SET tenkhoa=%s, truongkhoa=%s, sdt=%s WHERE makhoa=%s"
            cursor.execute(sql, (name, head, phone, fid))
            if cursor.rowcount == 0:
                messagebox.showerror("Lỗi", "Không tìm thấy khoa để cập nhật.")
            else:
                conn.commit()
                # cập nhật cache nếu tồn tại
                for f in self.faculties:
                    if f.get("makhoa") == fid:
                        f["tenkhoa"] = name
                        f["truongkhoa"] = head
                        f["sdt"] = phone
                        break
                self.refresh_list()
                self.clear_form()
                messagebox.showinfo("Thành công", "Đã cập nhật thông tin khoa.")
            cursor.close()
        except Exception as e:
            messagebox.showerror("Lỗi cập nhật", f"Không thể cập nhật khoa:\n{e}")
        finally:
            try:
                conn.close()
            except:
                pass

    def delete_faculty(self):
        fid = self.entry_id.get().strip()
        if not fid:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng chọn khoa cần xóa!")
            return

        if not messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa khoa {fid}?"):
            return

        conn = get_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            sql = "DELETE FROM khoa WHERE makhoa=%s"
            cursor.execute(sql, (fid,))
            if cursor.rowcount == 0:
                messagebox.showerror("Lỗi", "Không tìm thấy khoa để xóa.")
            else:
                conn.commit()
                # cập nhật cache
                self.faculties = [f for f in self.faculties if f.get("makhoa") != fid]
                self.refresh_list()
                self.clear_form()
                messagebox.showinfo("Thành công", "Đã xóa khoa.")
            cursor.close()
        except Exception as e:
            messagebox.showerror("Lỗi xóa", f"Không thể xóa khoa:\n{e}")
        finally:
            try:
                conn.close()
            except:
                pass

    def clear_all(self):
        if not messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa toàn bộ danh sách khoa trong database?"):
            return

        conn = get_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM khoa")
            conn.commit()
            cursor.close()
            self.faculties.clear()
            self.refresh_list()
            self.clear_form()
            messagebox.showinfo("Thành công", "Đã xóa toàn bộ danh sách khoa.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xóa toàn bộ:\n{e}")
        finally:
            try:
                conn.close()
            except:
                pass

    # ---------------- chọn dòng trong list ----------------
    def select_faculty(self, event=None):
        try:
            line = self.listbox.get("insert linestart", "insert lineend")
            parts = line.split(".")
            if len(parts) < 2:
                return
            right = parts[1].strip()
            makhoa = right.split("-")[0].strip()
            rec = next((f for f in self.faculties if f.get("makhoa") == makhoa), None)
            if rec:
                self.entry_id.delete(0, END); self.entry_id.insert(0, rec.get("makhoa", ""))
                self.entry_name.delete(0, END); self.entry_name.insert(0, rec.get("tenkhoa", ""))
                self.entry_head.delete(0, END); self.entry_head.insert(0, rec.get("truongkhoa", ""))
                self.entry_phone.delete(0, END); self.entry_phone.insert(0, rec.get("sdt", ""))
        except Exception:
            pass

    def clear_form(self):
        for entry in (self.entry_id, self.entry_name, self.entry_head, self.entry_phone):
            entry.delete(0, END)
