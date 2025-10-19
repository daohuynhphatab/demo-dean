from tkinter import *
from database import *
def show():
    sv = read()
    listbox.delete(0, END)
    for i in sv:
        listbox.insert(END, i)
def add():
    line = svid.get() + '-' + name.get()
    save(line)
    show()


root = Tk()
#var
svid= StringVar()
name= StringVar()
root.title("Quản Lý Sinh Viên")
root.minsize(500, 500)
Label(root, text="Quản Lý Sinh Viên", font=("Arial", 24)).grid(row=0)
listbox=Listbox(root,width=80, height=20)
listbox.grid(row=1, columnspan= 2)
show()
Label(root, text="Họ và tên:").grid(row=2, column=0)
Entry(root, textvariable=name).grid(row=2, column=1)
Label(root, text="Mã sinh viên:").grid(row=3, column=0)
Entry(root, textvariable=svid).grid(row=3, column=1)
button= Frame(root)
Button(button, text="Thêm", command=add).pack(side=LEFT)
Button(button, text="Xóa").pack(side=LEFT)
Button(button, text="Sửa").pack(side=LEFT)
Button(button, text="Thoát", command=root.quit).pack(side=LEFT)
Button.grid(button, row=4, column=1)
root.mainloop()
