import mysql.connector

def get_connection():
    return mysql.connector.connect(host='localhost', user='root',password='123456',database='qlsv')
def save(line):
    masv, hoten, ngaysinh, gioitinh, diachi, sdt, malop = line.split('-')
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO sinhvien (MaSV, HoTen, NgaySinh, GioiTinh, DiaChi, SDT, MaLop) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (masv, hoten, ngaysinh, gioitinh, diachi, sdt, malop))
    conn.commit()
    conn.close()


def read():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT MASOSV, HOVATEN, NGAYSINH, GIOITINH, DIACHI, SDT, MALOP FROM sinhvien")
    sv = cursor.fetchall()  # trả về list các tuple [(masv, hoten), ...]
    conn.close()
    return sv


def overwrite(data_list):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sinhvien")  # xoá hết bảng
    sql = "INSERT INTO sinhvien (MaSV, HoTen) VALUES (%s, %s)"
    cursor.executemany(sql, data_list)
    conn.commit()
    conn.close()

def delete_student(masv):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sinhvien WHERE MaSV=%s", (masv,))
    conn.commit()
    conn.close()

def update_student(old_id, new_id, new_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE sinhvien SET MaSV=%s, HoTen=%s WHERE MaSV=%s", (new_id, new_name, old_id))
    conn.commit()
    conn.close()