import mysql.connector
from tkinter import messagebox

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='123456',
            database='qlsv'
        )
        return connection
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
        return None