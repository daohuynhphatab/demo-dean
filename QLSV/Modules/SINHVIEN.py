import customtkinter as ctk
import tkinter.ttk as ttk
from tkinter import messagebox, END, filedialog
from PIL import Image, ImageTk 
from Modules.database import get_connection
import os 

class StudentManagerFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.selected_image_path = None #Lưu đường dẫn ảnh đã chọn
        self.photo_tk = None # Tham chiếu ảnh

        self.face_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'face') #Xác định thư mục 'face'
        if not os.path.exists(self.face_dir):
            os.makedirs(self.face_dir, exist_ok=True) #Tạo thư mục nếu chưa tồn tại

        # === Tiêu đề ===
        title = ctk.CTkLabel(self, text="Quản lý sinh viên", font=ctk.CTkFont(size=20, weight="bold"))
        title.grid(row=0, column=0, columnspan=2, pady=10)

        # === Frame tổng chứa form + bảng ===
        content_frame = ctk.CTkFrame(self)
        content_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(1, weight=1)

        # === Form nhập + ảnh ===
        top_frame = ctk.CTkFrame(content_frame)
        top_frame.grid(row=0, column=0, sticky="nw", pady=(0,10))

        # === Form nhập thông tin ===
        form_frame = ctk.CTkFrame(top_frame)
        form_frame.grid(row=0, column=0, padx=(0,20), sticky="nw")

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

        # Frame ảnh sinh viên
        img_frame = ctk.CTkFrame(top_frame)
        img_frame.grid(row=0, column=1, padx=10, sticky="ne")

        self.photo_label = ctk.CTkLabel(img_frame, text="(Chưa có ảnh)", width=120, height=120, fg_color="#3a3a3a")
        self.photo_label.grid(row=0, column=0, pady=5)

        # === Nút chức năng ===
        btn_frame = ctk.CTkFrame(form_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)

        ctk.CTkButton(btn_frame, text="Thêm", command=self.add_student).grid(row=0, column=1, padx=5)
        ctk.CTkButton(btn_frame, text="Sửa", command=self.update_student).grid(row=0, column=2, padx=5)
        ctk.CTkButton(btn_frame, text="Xóa", command=self.delete_student).grid(row=0, column=3, padx=5)
        ctk.CTkButton(img_frame, text="Chọn ảnh", command=self.select_image).grid(row=1, column=0, pady=5)

        # === Bảng hiển thị danh sách sinh viên ===
        table_frame = ctk.CTkFrame(content_frame)
        table_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#2b2b2b",
                        foreground="white",
                        font=("Segoe UI", 18),
                        rowheight=50,
                        fieldbackground="#2b2b2b"
                        )
        style.configure("Treeview.Heading",
                        background="#1f538d",
                        foreground="white",
                        font=("Segoe UI", 18, "bold")
                        )
        style.map('Treeview', background=[('selected', '#1f538d')])

        self.tree = ttk.Treeview(
            table_frame,
            columns=("masv", "hoten", "malop", "khoa", "image_link"), 
            show="headings",
            selectmode="browse"
        )
        self.tree.heading("masv", text="Mã SV")
        self.tree.heading("hoten", text="Họ tên")
        self.tree.heading("malop", text="Mã lớp")
        self.tree.heading("khoa", text="Khoa")
        self.tree.heading("image_link", text="Đường dẫn ảnh") 

        self.tree.column("masv", width=100, anchor="center")
        self.tree.column("hoten", width=200)
        self.tree.column("malop", width=100, anchor="center")
        self.tree.column("khoa", width=100, anchor="center")
        self.tree.column("image_link", width=0, stretch=False)

        self.tree.grid(row=0, column=0, sticky="nsew")

        # Scrollbar dọc
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Tải dữ liệu ban đầu
        self.load_students()

        self.tree.bind("<<TreeviewSelect>>", self.select_class)


    # === Tải danh sách sinh viên ===
    def load_students(self):
        """Tải danh sách sinh viên từ DB vào cache self.students rồi refresh GUI."""
        conn = get_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("SELECT id, name, faculty, classid, image_link FROM sinhvien ORDER BY id") 
            rows = cursor.fetchall()
            self.students = rows
            cursor.close()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tải danh sách sinh viên:\n{e}")
            self.students = []
        finally:
            try:
                conn.close()
            except:
                pass
        
        self.refresh_list()


    def refresh_list(self):
        """Hiển thị self.students lên Treeview."""
        self.tree.delete(*self.tree.get_children())

        
        for i, c in enumerate(self.students, start=1):
            self.tree.insert("", "end", values=(
                c["id"],        
                c["name"],     
                c["classid"],  
                c["faculty"],   
                c["image_link"] 
            ))


    # === Thêm sinh viên ===
    def add_student(self):
        sid = self.entry_id.get().strip()
        name = self.entry_name.get().strip()
        sclass = self.entry_class.get().strip() 
        faculty = self.entry_faculty.get().strip() 
        image_link = self.selected_image_path if self.selected_image_path else "" 
        

        if not sid or not name or not sclass or not faculty:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin!")
            return

        conn = get_connection()
        if not conn:
            return

        cursor = conn.cursor()
        try:
            
            cursor.execute(
                "INSERT INTO sinhvien (id, name, faculty, classid, image_link) VALUES (%s, %s, %s, %s, %s)",
                (sid, name, faculty, sclass, image_link)
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

        img_path = self.selected_image_path if self.selected_image_path else "" 

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
                "UPDATE sinhvien SET name=%s, faculty=%s, classid=%s, image_link=%s WHERE id=%s",
                (name, faculty, sclass, img_path, sid)
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
    def select_class(self, event=None):
        try:
            selected_item = self.tree.selection()
            if not selected_item:
                return

            item_values = self.tree.item(selected_item, "values")

            masv, hoten, malop, khoa, image_link = item_values

            self.entry_id.delete(0, END)
            self.entry_id.insert(0, masv)

            self.entry_name.delete(0, END)
            self.entry_name.insert(0, hoten)

            self.entry_class.delete(0, END)
            self.entry_class.insert(0, malop)

            self.entry_faculty.delete(0, END)
            self.entry_faculty.insert(0, khoa)

            img_path = image_link
            
            # Hiển thị ảnh nếu có 
            if img_path:
                self.display_image(img_path) 
            else:
                self.clear_image()

        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi chọn sinh viên:\n{e}")
            self.clear_image()


    def clear_form(self):
        for entry in (self.entry_id, self.entry_name, self.entry_class, self.entry_faculty):
            entry.delete(0, END)
        self.clear_image() 

    # === Chọn ảnh đại diện ===
    def select_image(self):
        """Mở hộp thoại chọn file ảnh, bắt đầu từ thư mục 'face'."""
        file_path = filedialog.askopenfilename(
            title="Chọn ảnh",
            initialdir=self.face_dir, 
            filetypes=[("Image files", "*.png *.jpg *.jpeg")]
        )
        if file_path:
            self.selected_image_path = file_path
            
            # Tải ảnh, resize, và chuyển thành CTkImage
            try:
                img = Image.open(file_path)
                img = img.resize((120, 120), Image.LANCZOS) 
                
                # Sử dụng ctk.CTkImage để tránh cảnh báo HighDPI
                self.photo_tk = ctk.CTkImage(light_image=img, dark_image=img, size=(120, 120))
                
                self.photo_label.configure(image=self.photo_tk, text="")
                self.photo_label.image = self.photo_tk 
                
            except Exception as e:
                messagebox.showerror("Lỗi Ảnh", f"Không thể tải hoặc hiển thị ảnh:\n{e}")
                self.selected_image_path = None

# Các hàm mới để chuẩn hóa việc tải, resize, và hiển thị ảnh bằng ctk.CTkImage.

    def display_image(self, file_path):
        """Tải và hiển thị ảnh lên photo_label."""
        if os.path.exists(file_path):
            try:
                img = Image.open(file_path)
                img = img.resize((120, 120), Image.LANCZOS)
                
                # Sử dụng ctk.CTkImage
                self.photo_tk = ctk.CTkImage(light_image=img, dark_image=img, size=(120, 120))
                
                self.photo_label.configure(image=self.photo_tk, text="")
                self.photo_label.image = self.photo_tk 
                self.selected_image_path = file_path 
            except Exception as e:
                self.clear_image()
                print(f"Lỗi tải ảnh: {e}")
        else:
            self.clear_image()

    def clear_image(self):
        """Xóa ảnh trên photo_label."""
        self.photo_label.configure(image="", text="(Chưa có ảnh)")
        self.photo_tk = None
        self.selected_image_path = None