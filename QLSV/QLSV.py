from tkinter import *
from tkinter import messagebox
from database import *

root = Tk()
root.title("Quản Lý Sinh Viên")
root.minsize(500, 500)

# --- VAR ---
svid = StringVar()
name = StringVar()

# --- FUNCTION ---
def show():
    listbox.delete(0, END)
    sv = read()
    for i in sv:
        listbox.insert(END, f"{i[0]} - {i[1]}")

def add():
    ma = svid.get().strip()
    ten = name.get().strip()
    if not ma or not ten:
        messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ Mã SV và Họ Tên!")
        return
    save(f"{ma}-{ten}")
    show()
    clear_form()

def delete():
    selected = listbox.curselection()
    if not selected:
        messagebox.showinfo("Chọn dòng", "Vui lòng chọn sinh viên cần xóa.")
        return
    index = selected[0]
    sv = read()
    del sv[index]
    overwrite(sv)
    show()
    clear_form()

def edit():
    selected = listbox.curselection()
    if not selected:
        messagebox.showinfo("Chọn dòng", "Vui lòng chọn sinh viên cần sửa.")
        return
    index = selected[0]
    sv = read()
    ma = svid.get().strip()
    ten = name.get().strip()
    if not ma or not ten:
        messagebox.showwarning("Thiếu thông tin", "Nhập mã và tên mới để cập nhật.")
        return
    sv[index] = [ma, ten]
    overwrite(sv)
    show()
    clear_form()

def clear_form():
    svid.set("")
    name.set("")

def select_item(event):
    selected = listbox.curselection()
    if selected:
        index = selected[0]
        sv = read()
        svid.set(sv[index][0])
        name.set(sv[index][1])

# --- UI ---
Label(root, text="Quản Lý Sinh Viên", font=("Arial", 24)).grid(row=0, columnspan=2, pady=10)

listbox = Listbox(root, width=80, height=20)
listbox.grid(row=1, columnspan=2)
listbox.bind("<<ListboxSelect>>", select_item)

Label(root, text="Mã sinh viên:").grid(row=2, column=0, sticky=W, padx=10)
Entry(root, textvariable=svid, width=30).grid(row=2, column=1, sticky=W)

Label(root, text="Họ và tên:").grid(row=3, column=0, sticky=W, padx=10)
Entry(root, textvariable=name, width=30).grid(row=3, column=1, sticky=W)

frame_btn = Frame(root)
frame_btn.grid(row=4, column=1, pady=15, sticky=E)

Button(frame_btn, text="Thêm", command=add, width=10).pack(side=LEFT, padx=5)
Button(frame_btn, text="Xóa", command=delete, width=10).pack(side=LEFT, padx=5)
Button(frame_btn, text="Sửa", command=edit, width=10).pack(side=LEFT, padx=5)
Button(frame_btn, text="Thoát", command=root.quit, width=10).pack(side=LEFT, padx=5)

show()
root.mainloop()