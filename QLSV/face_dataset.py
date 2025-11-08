import customtkinter as ctk
import cv2
import os
from database import get_connection  

# Hàm để chụp ảnh khuôn mặt
def capture_face_image(student_id):
    video_capture = cv2.VideoCapture(0)
    print("Nhấn 'q' để chụp ảnh. Nhấn 'Esc' để thoát.")
    
    if not video_capture.isOpened():
        print("Không thể mở camera. Vui lòng kiểm tra kết nối camera của bạn.")
        return None

    while True:
        ret, frame = video_capture.read()
        
        if not ret:
            print("Không thể đọc khung hình từ camera.")
            break

        cv2.imshow('Video', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            image_path = f'face_images/{student_id}.jpg'
            cv2.imwrite(image_path, frame)
            print(f'Ảnh đã được lưu: {image_path}')
            break
        
        if cv2.waitKey(1) & 0xFF == 27:
            break

    video_capture.release()
    cv2.destroyAllWindows()
    return image_path  # Trả về đường dẫn ảnh

# Hàm để lưu ảnh vào cơ sở dữ liệu
def insert_face_image(student_id, image_path):
    with open(image_path, 'rb') as file:
        binary_data = file.read()

    db = get_connection()
    cursor = db.cursor()
    
    sql = "INSERT INTO face_image (student_id, image_path, created_at) VALUES (%s, %s, NOW())"
    values = (student_id, image_path)
    
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    
    print(f'Hình ảnh của sinh viên ID {student_id} đã được lưu vào cơ sở dữ liệu.')

