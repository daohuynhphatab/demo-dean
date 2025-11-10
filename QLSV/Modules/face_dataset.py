import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk
import os

class AttendanceFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # === Tiêu đề ===
        title = ctk.CTkLabel(self, text="Điểm danh sinh viên", font=ctk.CTkFont(size=24, weight="bold"))
        title.grid(row=0, column=0, columnspan=2, pady=20)

        # === Nhập mã sinh viên ===
        self.entry_id = ctk.CTkEntry(self, placeholder_text="Nhập mã sinh viên...")
        self.entry_id.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        btn_search = ctk.CTkButton(self, text="Tìm sinh viên", command=self.load_student_info)
        btn_search.grid(row=1, column=1, padx=20, pady=10)

        # === Ảnh ===
        self.img_label_db = ctk.CTkLabel(self, text="Ảnh trong cơ sở dữ liệu")
        self.img_label_db.grid(row=2, column=0, padx=20, pady=10)
        self.img_label_input = ctk.CTkLabel(self, text="Ảnh nhập vào")
        self.img_label_input.grid(row=2, column=1, padx=20, pady=10)

        self.lbl_db_img = ctk.CTkLabel(self, text="(Chưa có ảnh)")
        self.lbl_db_img.grid(row=3, column=0, padx=20, pady=10)

        self.lbl_input_img = ctk.CTkLabel(self, text="(Chưa có ảnh)")
        self.lbl_input_img.grid(row=3, column=1, padx=20, pady=10)

        btn_upload = ctk.CTkButton(self, text="Tải ảnh mới", command=self.upload_image)
        btn_upload.grid(row=4, column=1, pady=10)

        # === Thông tin sinh viên ===
        self.info_label = ctk.CTkLabel(self, text="Thông tin sinh viên sẽ hiển thị tại đây", justify="left")
        self.info_label.grid(row=5, column=0, columnspan=2, pady=20)

        # === Nút điểm danh ===
        btn_check = ctk.CTkButton(self, text="✅ Xác nhận điểm danh", command=self.mark_attendance)
        btn_check.grid(row=6, column=0, columnspan=2, pady=10)

        # === Biến lưu ===
        self.selected_image_path = None
        self.current_student = None

    def load_student_info(self):
        student_id = self.entry_id.get().strip()
        if not student_id:
            self.info_label.configure(text="⚠️ Hãy nhập mã sinh viên.")
            return

        # === (Tạm) Dữ liệu mẫu, sau này sẽ truy DB ===
        if student_id == "SV01":
            self.current_student = {
                "masv": "SV01",
                "hoten": "Nguyễn Văn A",
                "lop": "CTK45",
                "khoa": "CNTT",
                "image_path": "images/SV01.jpg"
            }
        else:
            self.current_student = None

        if self.current_student:
            self.info_label.configure(
                text=f"📘 Mã SV: {self.current_student['masv']}\n"
                     f"Họ tên: {self.current_student['hoten']}\n"
                     f"Lớp: {self.current_student['lop']}\n"
                     f"Khoa: {self.current_student['khoa']}"
            )
            # Hiển thị ảnh DB
            img_path = self.current_student["image_path"]
            if os.path.exists(img_path):
                img = Image.open(img_path).resize((200, 200))
                tk_img = ImageTk.PhotoImage(img)
                self.lbl_db_img.configure(image=tk_img, text="")
                self.lbl_db_img.image = tk_img
            else:
                self.lbl_db_img.configure(text="(Không tìm thấy ảnh)")
        else:
            self.info_label.configure(text="❌ Không tìm thấy sinh viên!")

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Ảnh", "*.jpg;*.png")])
        if file_path:
            self.selected_image_path = file_path
            img = Image.open(file_path).resize((200, 200))
            tk_img = ImageTk.PhotoImage(img)
            self.lbl_input_img.configure(image=tk_img, text="")
            self.lbl_input_img.image = tk_img

    def mark_attendance(self):
        if not self.current_student:
            self.info_label.configure(text="⚠️ Chưa có thông tin sinh viên để điểm danh.")
            return
        if not self.selected_image_path:
            self.info_label.configure(text="⚠️ Chưa chọn ảnh để so sánh.")
            return

        # Giả lập kiểm tra khuôn mặt (sau sẽ thay bằng model thực)
        self.info_label.configure(
            text=f"✅ Điểm danh thành công cho {self.current_student['hoten']}!"
        )
