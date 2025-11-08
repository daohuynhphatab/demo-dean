import customtkinter as ctk
import cv2
import os

from SINHVIEN import StudentManagerFrame
from LOP import ClassManagerFrame
from KHOA import FacultyManagerFrame

# === Config ===
ctk.set_appearance_mode("System")  # or "Dark" / "Light"
ctk.set_default_color_theme("blue")

APP_TITLE = "Quản Lý Sinh Viên"
WINDOW_SIZE = "1000x750"

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(WINDOW_SIZE)

        # Grid setup
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Sidebar
        sidebar = ctk.CTkFrame(self, width=180)
        sidebar.grid(row=0, column=0, sticky="nswe")
        sidebar.grid_rowconfigure(5, weight=1)

        logo = ctk.CTkLabel(sidebar, text="QLSV", font=ctk.CTkFont(size=24, weight="bold"))
        logo.grid(row=0, column=0, pady=12)

        btn_students = ctk.CTkButton(sidebar, text="Quản lý sinh viên", command=self.show_students)
        btn_students.grid(row=1, column=0, sticky="ew", padx=12, pady=6)
        btn_classes = ctk.CTkButton(sidebar, text="Quản lý lớp học", command=self.show_classes)
        btn_classes.grid(row=2, column=0, sticky="ew", padx=12, pady=6)
        btn_faculties = ctk.CTkButton(sidebar, text="Quản lý khoa", command=self.show_faculties)
        btn_faculties.grid(row=3, column=0, sticky="ew", padx=12, pady=6)
        
        btn_capture_image = ctk.CTkButton(sidebar, text="Chụp ảnh", command=self.capture_face_image)
        btn_capture_image.grid(row=4, column=0, sticky="ew", padx=12, pady=6)

        self.mode_switch = ctk.CTkSwitch(sidebar, text="Dark mode", command=self.toggle_mode)
        self.mode_switch.grid(row=5, column=0, padx=12, pady=6, sticky="s")

        # Content area
        content = ctk.CTkFrame(self)
        content.grid(row=0, column=1, sticky="nswe", padx=12, pady=12)
        content.grid_rowconfigure(0, weight=1)
        content.grid_columnconfigure(0, weight=1)

        # Instantiate module frames
        self.student_frame = StudentManagerFrame(content)
        self.class_frame = ClassManagerFrame(content)
        self.faculty_frame = FacultyManagerFrame(content)

        for f in (self.student_frame, self.class_frame, self.faculty_frame):
            f.grid(row=0, column=0, sticky="nswe")

        # Show students by default
        self.show_students()

    def show_students(self):
        self.student_frame.tkraise()

    def show_classes(self):
        self.class_frame.tkraise()

    def show_faculties(self):
        self.faculty_frame.tkraise()

    def toggle_mode(self):
        if self.mode_switch.get():
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")
    
    def capture_face_image(self):
        student_id = "12345"  # Bạn sẽ cần cách nào để biết ID sinh viên, có thể lấy từ giao diện
        os.makedirs("face_images", exist_ok=True)  # Tạo thư mục nếu chưa tồn tại

        # Mở camera
        video_capture = cv2.VideoCapture(0)
        
        if not video_capture.isOpened():
            print("Không thể mở camera. Vui lòng kiểm tra kết nối camera của bạn.")
            return

        print("Nhấn 'q' để chụp ảnh. Nhấn 'Esc' để thoát.")
        
        while True:
            ret, frame = video_capture.read()
            
            if not ret:
                print("Không thể đọc khung hình từ camera.")
                break

            cv2.imshow('Video', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                # Lưu ảnh
                image_path = f'face_images/{student_id}.jpg'
                cv2.imwrite(image_path, frame)
                print(f'Ảnh đã được lưu: {image_path}')
                break
            
            if cv2.waitKey(1) & 0xFF == 27:
                break

        video_capture.release()
        cv2.destroyAllWindows()
    

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()