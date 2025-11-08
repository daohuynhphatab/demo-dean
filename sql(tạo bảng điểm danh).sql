CREATE DATABASE IF NOT EXISTS qlsv;
USE qlsv;
-- bảng lưu ảnh 
CREATE TABLE face_image (
  face_id INT AUTO_INCREMENT PRIMARY KEY,
  student_id VARCHAR(20) NOT NULL,
  image_path VARCHAR(500) NOT NULL,      -- đường dẫn file ảnh lưu trên filesystem
  embedding LONGBLOB NOT NULL,           -- lưu numpy bytes (float32) hoặc json text
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (student_id) REFERENCES sinhvien(id) ON DELETE CASCADE
);

-- bảng buổi điểm danh
CREATE TABLE attendance_session (
  session_id INT AUTO_INCREMENT PRIMARY KEY,
  malop VARCHAR(20) NOT NULL, 
  subject VARCHAR(200),
  session_date DATE NOT NULL,
  start_time TIME,
  end_time TIME,
  location VARCHAR(200),
  created_by VARCHAR(50),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (malop) REFERENCES lop(malop) ON DELETE CASCADE
);

-- bảng kết quả điểm danh
CREATE TABLE attendance_record (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  session_id INT NOT NULL,
  student_id VARCHAR(20) NOT NULL,
  status ENUM('present','absent','late','excused') DEFAULT 'present',
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  confidence FLOAT DEFAULT NULL,           -- độ tin cậy từ việc match
  snapshot_path VARCHAR(500) DEFAULT NULL, -- ảnh snapshot lúc điểm danh
  matched_face_id INT DEFAULT NULL,        -- face_image.face_id nếu có
  created_by VARCHAR(50),                  -- ai (giảng viên/hệ thống) xác nhận
  note VARCHAR(300),
  FOREIGN KEY (session_id) REFERENCES attendance_session(session_id) ON DELETE CASCADE,
  FOREIGN KEY (student_id) REFERENCES sinhvien(id) ON DELETE CASCADE,
  FOREIGN KEY (matched_face_id) REFERENCES face_image(face_id) ON DELETE SET NULL
);