 #database.py
import mysql.connector
import customtkinter as ctk
def get_connection():
    
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",  # đổi lại nếu khác
            database="qlsv"
        )
        return conn
   