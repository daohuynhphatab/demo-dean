import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import os
import face_recognition # Thư viện nhận dạng khuôn mặt
import mysql.connector # Cần để xử lý lỗi DB
from Modules.database import get_connection 
import cv2 # THƯ VIỆN XỬ LÝ ẢNH VÀ WEBCAM
import datetime # DÙNG ĐỂ TẠO TÊN FILE ẢNH DUY NHẤT


class AttendanceFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.current_student = None
        self.selected_image_path = None
        self.tk_img_db = None 
        self.tk_img_input = None 

        # === Tiêu đề ===
        title = ctk.CTkLabel(self, text="Điểm danh sinh viên", font=ctk.CTkFont(size=24, weight="bold"))
        title.grid(row=0, column=0, columnspan=2, pady=20)

        # === Nhập mã sinh viên ===
        self.entry_id = ctk.CTkEntry(self, placeholder_text="Nhập mã sinh viên...")
        self.entry_id.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        btn_search = ctk.CTkButton(self, text="Tìm sinh viên", command=self.load_student_info)
        btn_search.grid(row=1, column=1, padx=20, pady=10)

        self.info_label = ctk.CTkLabel(self, text="Thông tin sinh viên sẽ hiển thị ở đây", wraplength=450, justify="left")
        self.info_label.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        # Frame chứa ảnh
        img_frame = ctk.CTkFrame(self)
        img_frame.grid(row=3, column=0, columnspan=2, padx=20, pady=10)
        
        ctk.CTkLabel(img_frame, text="Ảnh trong Cơ sở dữ liệu").grid(row=0, column=0, padx=20, pady=5)
        self.lbl_db_img = ctk.CTkLabel(img_frame, text="(Ảnh DB)", width=200, height=200, fg_color="#3a3a3a")
        self.lbl_db_img.grid(row=1, column=0, padx=20, pady=5)
        
        ctk.CTkLabel(img_frame, text="Ảnh chụp/Tải lên").grid(row=0, column=1, padx=20, pady=5)
        self.lbl_input_img = ctk.CTkLabel(img_frame, text="(Ảnh Input)", width=200, height=200, fg_color="#3a3a3a")
        self.lbl_input_img.grid(row=1, column=1, padx=20, pady=5)

        # Nút chức năng
        btn_frame = ctk.CTkFrame(self)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)

        ctk.CTkButton(btn_frame, text="Tải ảnh điểm danh", command=self.upload_image).grid(row=0, column=0, padx=10)
        ctk.CTkButton(btn_frame, text="📸 Chụp ảnh (Webcam)", command=self.capture_image_webcam).grid(row=0, column=1, padx=10)
        ctk.CTkButton(btn_frame, text="✔️ Điểm danh & So sánh", command=self.mark_attendance).grid(row=0, column=2, padx=10)


    # === HÀM TRUY VẤN DB ĐÃ SỬA LỖI TÊN CỘT CHÍNH XÁC VÀ ALIAS ===
    def _fetch_student_info(self, masv):
        """Tải thông tin sinh viên từ DB bằng cách JOIN 3 bảng."""
        conn = get_connection()
        if not conn:
            messagebox.showerror("Lỗi Nối Kết", "Không thể kết nối đến cơ sở dữ liệu.")
            return None
        try:
            cursor = conn.cursor(dictionary=True) 
            
            # SỬ DỤNG TÊN CỘT THỰC TẾ TRONG DB VÀ DÙNG ALIAS (AS)
            query = """
                SELECT 
                    sv.id, 
                    sv.name,         
                    sv.name,               
                    sv. classid,      
                    sv.faculty,     
                    sv.image_link
                FROM 
                    sinhvien sv
                JOIN 
                    lop l ON sv.classid = l.malop  -- SỬ DỤNG sv.malop để JOIN
                JOIN 
                    khoa k ON l.makhoa = k.makhoa
                WHERE 
                    sv.id = %s
            """
            cursor.execute(query, (masv,))
            student = cursor.fetchone()
            
            if student:
                student['image_path'] = student.pop('image_link')
            
            return student
        except mysql.connector.Error as e:
            print(f"Lỗi truy vấn DB: {e}")
            messagebox.showerror("Lỗi DB", f"Không thể tải thông tin sinh viên: {e}")
            return None
        finally:
            if conn and conn.is_connected():
                conn.close()

    # Hàm trợ giúp hiển thị ảnh Input/Webcam
    def _display_input_image(self, file_path):
        try:
            img = Image.open(file_path).resize((200, 200), Image.LANCZOS)
            self.tk_img_input = ctk.CTkImage(light_image=img, dark_image=img, size=(200, 200))
            self.lbl_input_img.configure(image=self.tk_img_input, text="")
            self.lbl_input_img.image = self.tk_img_input
        except Exception as e:
            messagebox.showerror("Lỗi Ảnh", f"Không thể hiển thị ảnh vừa chụp: {e}")
            self.lbl_input_img.configure(image=None, text="(Lỗi hiển thị)")
            self.tk_img_input = None
            self.selected_image_path = None


    # Hàm load student info 
    def load_student_info(self):
        self.clear_images()
        masv = self.entry_id.get().strip()
        if not masv:
            self.info_label.configure(text="⚠️ Vui lòng nhập Mã sinh viên.")
            return

        student = self._fetch_student_info(masv) 

        if student:
            self.current_student = student
            self.info_label.configure(
                text=(f"✅ Tìm thấy: {student['name']} (ID: {student['id']})\n" 
                      f"Mã lớp: {student['classid']}\n"   
                      f"Tên Khoa: {student['faculty']}")  
            )
            
            # Hiển thị ảnh DB (image_face)
            img_path = self.current_student.get("image_path")
            if not img_path or not os.path.exists(img_path):
                self.info_label.configure(text=self.info_label.cget("text") + "\n⚠️ Chưa có ảnh khuôn mặt DB! Vui lòng tải ảnh.")
                self.lbl_db_img.configure(image=None, text="(Không tìm thấy ảnh)")
                self.tk_img_db = None
                return 
            
            # Load và hiển thị ảnh DB
            try:
                img = Image.open(img_path).resize((200, 200), Image.LANCZOS)
                self.tk_img_db = ctk.CTkImage(light_image=img, dark_image=img, size=(200, 200))
                self.lbl_db_img.configure(image=self.tk_img_db, text="")
                self.lbl_db_img.image = self.tk_img_db
            except Exception as e:
                self.info_label.configure(text=f"❌ Lỗi đọc ảnh DB: {e}")
                self.lbl_db_img.configure(image=None, text="(Lỗi đọc ảnh)")
                self.tk_img_db = None
        else:
            self.info_label.configure(text="❌ Không tìm thấy sinh viên!")
            self.current_student = None
            self.clear_images()

    # Hàm tải ảnh input 
    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Ảnh", "*.jpg;*.png;*.jpeg")])
        if file_path:
            self.selected_image_path = file_path
            self._display_input_image(file_path) 
        else:
            self.selected_image_path = None
    

    # === HÀM CHỤP ẢNH TỪ WEBCAM (SỬ DỤNG OPENCV) ===
    def capture_image_webcam(self):
        # 1. Khởi tạo Webcam
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Lỗi Webcam", "Không thể mở Webcam. Vui lòng kiểm tra thiết bị.")
            return

        # Tạo tên file duy nhất trong thư mục hiện tại
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"webcam_capture_{timestamp}.jpg"
        
        saved = False

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Hiển thị frame trong cửa sổ OpenCV
            cv2.putText(frame, "Nhan 'S' de luu anh, 'Q' de thoat", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.imshow("Webcam Capture", frame)

            # Bấm 's' để lưu ảnh hoặc 'q' để thoát
            key = cv2.waitKey(1) & 0xFF
            if key == ord('s'):
                cv2.imwrite(file_name, frame)
                self.selected_image_path = os.path.abspath(file_name) # Lưu đường dẫn tuyệt đối
                saved = True
                break
            elif key == ord('q'):
                break

        # Giải phóng tài nguyên
        cap.release()
        cv2.destroyAllWindows()

        if saved:
            messagebox.showinfo("Thành công", f"Đã chụp và lưu ảnh tại: {self.selected_image_path}")
            # Tải ảnh vừa chụp lên giao diện CTk
            self._display_input_image(self.selected_image_path)
        else:
            self.selected_image_path = None
            # Đảm bảo không còn ảnh cũ trên giao diện nếu hủy chụp
            self.lbl_input_img.configure(image=None, text="(Ảnh Input)")
            self.tk_img_input = None
            messagebox.showinfo("Thông báo", "Đã hủy chụp ảnh.")


    # HÀM SO SÁNH VÀ ĐIỂM DANH
    def mark_attendance(self):
        if not self.current_student:
            self.info_label.configure(text="⚠️ Chưa có thông tin sinh viên để điểm danh.")
            return
        if not self.selected_image_path:
            self.info_label.configure(text="⚠️ Vui lòng tải lên ảnh chụp để điểm danh.")
            return

        db_img_path = self.current_student.get("image_path")
        input_img_path = self.selected_image_path
        
        if not db_img_path or not os.path.exists(db_img_path):
            self.info_label.configure(text="❌ Ảnh DB không tồn tại! Vui lòng cập nhật ảnh sinh viên.")
            return

        try:
            # === MÃ HÓA KHUÔN MẶT (ENCODING) ===
            db_image = face_recognition.load_image_file(db_img_path)
            db_face_encodings = face_recognition.face_encodings(db_image)

            if not db_face_encodings:
                self.info_label.configure(text="❌ Không tìm thấy khuôn mặt trong ảnh DB!")
                return
            known_face_encoding = db_face_encodings[0]

            input_image = face_recognition.load_image_file(input_img_path)
            input_face_encodings = face_recognition.face_encodings(input_image)

            if not input_face_encodings:
                self.info_label.configure(text="❌ Không tìm thấy khuôn mặt trong ảnh chụp!")
                return
            unknown_face_encoding = input_face_encodings[0]

        except Exception as e:
            self.info_label.configure(text=f"Lỗi xử lý khuôn mặt: {e}")
            return

        # === SO SÁNH KHUÔN MẶT ===
        results = face_recognition.compare_faces(
            [known_face_encoding], 
            unknown_face_encoding, 
            tolerance=0.6 
        )

        if results[0]:
            self.info_label.configure(text=f"✅ Điểm danh THÀNH CÔNG! Khuôn mặt khớp. ({self.current_student['name']})")           
        else:
            self.info_label.configure(text="❌ Điểm danh THẤT BẠI! Khuôn mặt không khớp.")
            
    def clear_images(self):
        self.lbl_db_img.configure(image=None, text="(Ảnh DB)")
        self.lbl_input_img.configure(image=None, text="(Ảnh Input)")
        self.tk_img_db = None
        self.tk_img_input = None
        self.selected_image_path = None
        self.info_label.configure(text="Thông tin sinh viên sẽ hiển thị ở đây")