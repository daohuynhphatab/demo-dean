import mysql.connector
db = mysql.connector.connect(host='localhost', user='root',password='123456',database='qlsv')
# Tạo cơ sở dữ liệu
code = 'CREATE DATABASE `qlsv`'

# Run code
mycursor = db.cursor()
mycursor.execute(code)