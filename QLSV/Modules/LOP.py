import customtkinter as ctk
import tkinter.ttk as ttk
from tkinter import messagebox, END, filedialog 
from PIL import Image 
from Modules.database import get_connection
import os 


class ClassManagerFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Biến lưu trữ đường dẫn ảnh và tham chiếu ảnh
        self.selected_image_path = None
        self.photo_tk = None # Biến giữ tham chiếu ảnh ctk.CTkImage

        # Khởi tạo đường dẫn thư mục 'face' và đảm bảo nó tồn tại
        self.face_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'face') 
        if not os.path.exists(self.face_dir):
            os.makedirs(self.face_dir, exist_ok=True)

        # === Tiêu đề ===
        title = ctk.CTkLabel(self, text="Quản lý lớp", font=ctk.CTkFont(size=20, weight="bold"))
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

        ctk.CTkLabel(form_frame, text="Mã lớp:").grid(row=0, column=0, sticky="w", pady=2)
        ctk.CTkLabel(form_frame, text="Tên lớp:").grid(row=1, column=0, sticky="w", pady=2)
        ctk.CTkLabel(form_frame, text="Mã khoa:").grid(row=2, column=0, sticky="w", pady=2)
        ctk.CTkLabel(form_frame, text="Cố vấn học tập:").grid(row=3, column=0, sticky="w", pady=2)

        self.entry_malop = ctk.CTkEntry(form_frame, width=200)
        self.entry_tenlop = ctk.CTkEntry(form_frame, width=200)
        self.entry_makhoa = ctk.CTkEntry(form_frame, width=200)
        self.entry_cvht = ctk.CTkEntry(form_frame, width=200)

        self.entry_malop.grid(row=0, column=1, pady=2)
        self.entry_tenlop.grid(row=1, column=1, pady=2)
        self.entry_makhoa.grid(row=2, column=1, pady=2)
        self.entry_cvht.grid(row=3, column=1, pady=2)

        # Frame ảnh đại diện
        img_frame = ctk.CTkFrame(top_frame)
        img_frame.grid(row=0, column=2, padx=10, sticky="ne")

        self.photo_label = ctk.CTkLabel(img_frame, text="(Chưa có ảnh)", width=120, height=120, fg_color="#3a3a3a")
        self.photo_label.grid(row=0, column=0, pady=5)

        ctk.CTkButton(img_frame, text="Chọn ảnh", command=self.select_image).grid(row=1, column=0, pady=5)

        # === Nút chức năng ===
        btn_frame = ctk.CTkFrame(form_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)

        ctk.CTkButton(btn_frame, text="Thêm", command=self.add_class).grid(row=0, column=0, padx=5)
        ctk.CTkButton(btn_frame, text="Sửa", command=self.update_class).grid(row=0, column=1, padx=5)
        ctk.CTkButton(btn_frame, text="Xóa", command=self.delete_class).grid(row=0, column=2, padx=5)

        # === Bảng hiển thị danh sách lớp ===
        table_frame = ctk.CTkFrame(content_frame)
        table_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#2b2b2b",
                        foreground="white",
                        font=("Segoe UI", 16),
                        rowheight=40,
                        fieldbackground="#2b2b2b"
                        )
        style.configure("Treeview.Heading",
                        background="#1f538d",
                        foreground="white",
                        font=("Segoe UI", 16, "bold")
                        )
        style.map('Treeview', background=[('selected', '#1f538d')])

        self.tree = ttk.Treeview(
            table_frame,
            columns=("malop", "tenlop", "makhoa", "cvht", "image_link"),
            show="headings",
            selectmode="browse"
        )
        self.tree.heading("malop", text="Mã Lớp")
        self.tree.heading("tenlop", text="Tên Lớp")
        self.tree.heading("makhoa", text="Mã Khoa")
        self.tree.heading("cvht", text="Cố Vấn")
        self.tree.heading("image_link", text="Đường dẫn ảnh") # Tên cột ẩn

        self.tree.column("malop", width=100, anchor="center")
        self.tree.column("tenlop", width=200)
        self.tree.column("makhoa", width=100, anchor="center")
        self.tree.column("cvht", width=150, anchor="center")
       
        self.tree.column("image_link", width=0, stretch=False) # Ẩn cột image_link

        self.tree.grid(row=0, column=0, sticky="nsew") 

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.tree.bind("<<TreeviewSelect>>", self.select_class)

        self.load_classes()


    # === Load danh sách lớp ===
    def load_classes(self):
        conn = get_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("SELECT malop, tenlop, makhoa, cvht, image_link FROM lop ORDER BY malop")
            self.classes = cursor.fetchall()
            cursor.close()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tải danh sách lớp:\n{e}")
            self.classes = []
        finally:
            conn.close()

        self.refresh_list()


    def refresh_list(self):
        self.tree.delete(*self.tree.get_children())
        for c in self.classes:         
            self.tree.insert("", "end", values=(c["malop"], c["tenlop"], c["makhoa"], c["cvht"], c["image_link"]))


    # === Thêm lớp ===
    def add_class(self):
        malop = self.entry_malop.get().strip()
        tenlop = self.entry_tenlop.get().strip()
        makhoa = self.entry_makhoa.get().strip()
        cvht = self.entry_cvht.get().strip()
        # Lấy đường dẫn ảnh
        image_link = self.selected_image_path if self.selected_image_path else "" 

        if not malop or not tenlop or not makhoa or not cvht:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin!")
            return

        conn = get_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO lop (malop, tenlop, makhoa, cvht, image_link) VALUES (%s, %s, %s, %s, %s)",
                            (malop, tenlop, makhoa, cvht, image_link))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã thêm lớp mới!")
            self.load_classes()
            self.clear_form()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể thêm lớp: {e}")
        finally:
            conn.close()


    # === Cập nhật lớp ===
    def update_class(self):
        malop = self.entry_malop.get().strip()
        tenlop = self.entry_tenlop.get().strip()
        makhoa = self.entry_makhoa.get().strip()
        cvht = self.entry_cvht.get().strip()
        # Lấy đường dẫn ảnh
        img_path = self.selected_image_path if self.selected_image_path else "" 

        if not malop:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng chọn lớp cần sửa!")
            return

        conn = get_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT malop FROM lop WHERE malop=%s", (malop,))
            if not cursor.fetchone():
                messagebox.showerror("Lỗi", "Không tìm thấy lớp này!")
                return

            cursor.execute("UPDATE lop SET tenlop=%s, makhoa=%s, cvht=%s, image_link=%s WHERE malop=%s",
                            (tenlop, makhoa, cvht, img_path, malop))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã cập nhật thông tin lớp!")
            self.load_classes()
            self.clear_form()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể cập nhật: {e}")
        finally:
            conn.close()


    # === Xóa lớp ===
    def delete_class(self):
        malop = self.entry_malop.get().strip()
        if not malop:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng chọn lớp cần xóa!")
            return

        if not messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa lớp {malop}?"):
            return

        conn = get_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM lop WHERE malop=%s", (malop,))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã xóa lớp!")
            self.load_classes()
            self.clear_form()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xóa lớp: {e}")
        finally:
            conn.close()


    # === Khi chọn dòng trong bảng ===
    def select_class(self, event=None):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        values = self.tree.item(selected_item, "values")
        if len(values) != 5:
            return

        malop, tenlop, makhoa, cvht, image_link = values
        self.entry_malop.delete(0, END)
        self.entry_malop.insert(0, malop)

        self.entry_tenlop.delete(0, END)
        self.entry_tenlop.insert(0, tenlop)

        self.entry_makhoa.delete(0, END)
        self.entry_makhoa.insert(0, makhoa)

        self.entry_cvht.delete(0, END)
        self.entry_cvht.insert(0, cvht)

        # Hiển thị ảnh
        if image_link:
            self.display_image(image_link) 
        else:
            self.clear_image()

    
    def clear_form(self):
        for entry in (self.entry_malop, self.entry_tenlop, self.entry_makhoa, self.entry_cvht):
            entry.delete(0, END)
        # Clear ảnh khi clear form
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
                
                # Sử dụng ctk.CTkImage
                self.photo_tk = ctk.CTkImage(light_image=img, dark_image=img, size=(120, 120))
                
                # Cập nhật label
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
                
                # FIX: Sử dụng ctk.CTkImage
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