import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from db_connection import connect_db

def generate_std_id():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(std_ID) FROM student")
    max_id = cursor.fetchone()[0]
    conn.close()
    return 1 if max_id is None else max_id + 1

def fetch_students():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student")
    records = cursor.fetchall()
    conn.close()
    student_list.delete(*student_list.get_children())
    for record in records:
        student_list.insert("", tk.END, values=record)

def insert_student():
    name = name_entry.get().strip()
    email = email_entry.get().strip()
    phone = phone_entry.get().strip()
    batch = batch_entry.get().strip()
    linkedin = linkedin_entry.get().strip()
    leetcode = leetcode_entry.get().strip()
    
    if name == "" or email == "" or phone == "" or batch == "":
        messagebox.showwarning("Warning", "Please enter all required details")
        return
    try:
        batch = int(batch)
    except ValueError:
        messagebox.showerror("Error", "Batch year must be a number!")
        return
    
    std_id = generate_std_id()
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO student (std_ID, Name, email, phone_no, Batch_year, LinkedIn_ID, LeetCode_ID) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                   (std_id, name, email, phone, batch, linkedin, leetcode))
    conn.commit()
    conn.close()
    fetch_students()
    messagebox.showinfo("Success", f"Student added successfully with ID {std_id}!")

def delete_student():
    selected_item = student_list.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a student to delete")
        return
    std_id = student_list.item(selected_item)['values'][0]
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM student WHERE std_ID=%s", (std_id,))
    conn.commit()
    conn.close()
    fetch_students()
    messagebox.showinfo("Success", "Student deleted successfully!")

def open_student_management():
    global name_entry, email_entry, phone_entry, batch_entry, linkedin_entry, leetcode_entry, student_list
    student_window = tk.Toplevel()
    student_window.title("Student Management")
    student_window.geometry("700x500")
    student_window.configure(bg="#f0f0f0")
    
    tk.Label(student_window, text="Student Management", font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#333").pack(pady=10)
    
    form_frame = tk.Frame(student_window, bg="#ffffff", padx=10, pady=10, relief=tk.RIDGE, bd=2)
    form_frame.pack(pady=10)
    
    labels = ["Name:", "Email:", "Phone:", "Batch Year:", "LinkedIn ID:", "LeetCode ID:"]
    entries = []
    for i, label in enumerate(labels):
        tk.Label(form_frame, text=label, font=("Arial", 10), bg="#ffffff").grid(row=i, column=0, pady=5, padx=10, sticky="w")
        entry = tk.Entry(form_frame, font=("Arial", 10))
        entry.grid(row=i, column=1, pady=5, padx=10)
        entries.append(entry)
    
    name_entry, email_entry, phone_entry, batch_entry, linkedin_entry, leetcode_entry = entries
    
    button_frame = tk.Frame(student_window, bg="#f0f0f0")
    button_frame.pack()
    
    add_btn = tk.Button(button_frame, text="➕ Add Student", font=("Arial", 12, "bold"), bg="#28a745", fg="white", padx=10, pady=5, command=insert_student)
    add_btn.grid(row=0, column=0, padx=10, pady=5)
    
    del_btn = tk.Button(button_frame, text="❌ Delete Student", font=("Arial", 12, "bold"), bg="#dc3545", fg="white", padx=10, pady=5, command=delete_student)
    del_btn.grid(row=0, column=1, padx=10, pady=5)
    
    refresh_btn = tk.Button(button_frame, text="🔄 Refresh", font=("Arial", 12, "bold"), bg="#007bff", fg="white", padx=10, pady=5, command=fetch_students)
    refresh_btn.grid(row=0, column=2, padx=10, pady=5)
    
    student_list = ttk.Treeview(student_window, columns=("ID", "Name", "Email", "Phone", "Batch", "LinkedIn", "LeetCode"), show="headings")
    student_list.pack(pady=10, fill=tk.BOTH, expand=True)
    
    for col in ("ID", "Name", "Email", "Phone", "Batch", "LinkedIn", "LeetCode"):
        student_list.heading(col, text=col)
        student_list.column(col, width=100, anchor="center")
    
    fetch_students()
    student_window.mainloop()