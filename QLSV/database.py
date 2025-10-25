import mysql.connector

def get_connection():
    try:
        connection =  mysql.connector.connect(host='localhost', user='root',password='123456',database='qlsv')
        if connection.is_connected():
            print("Kết nối thành công với cơ sở dữ liệu!")
            return connection
    except Exception as e:
        print(f"Error: {e}")
        return 

if __name__ == "__main__":
    conn = get_connection()
    # đóng kết nối sau khi sử dụng
    if conn:
      conn.close()




def add(MASOSV, HOVATEN, NGAYSINH, GIOITINH, DIACHI, SDT, MALOP):
    connection = get_connection()
    cursor = connection.cursor()
    
    sql = "INSERT INTO students (MASOSV, HOVATEN, NGAYSINH, GIOITINH, DIACHI,SDT,MALOP) VALUES (%s, %s, %s,%s, %s, %s, %S)"
    values = (MASOSV, HOVATEN, NGAYSINH, GIOITINH, DIACHI,SDT,MALOP)
    cursor.execute(sql, values)
    connection.commit()

    print(f"Sinh viên có {HOVATEN} đã được thêm vào thành công!")
    
    cursor.close()
    connection.close()

