import tkinter as tk
from tkinter import messagebox
from db_connection import connect_db

# Function to generate a unique std_ID without gaps
def generate_std_id():
    conn = connect_db()
    cursor = conn.cursor()
    
    # Find the next available std_ID
    cursor.execute("SELECT std_ID FROM student ORDER BY std_ID ASC")
    existing_ids = [row[0] for row in cursor.fetchall()]
    
    new_id = 1
    while new_id in existing_ids:
        new_id += 1  # Find the first missing ID in sequence

    conn.close()
    return new_id

# Function to insert a new student
def insert_student(name, email, phone, batch, linkedin, leetcode):
    try:
        batch = int(batch)  # Ensure batch year is an integer
    except ValueError:
        messagebox.showerror("Error", "Batch year must be a number!")
        return

    if name == "" or email == "" or phone == "":
        messagebox.showwarning("Warning", "Please enter all details")
        return

    std_id = generate_std_id()  # Generate unique std_ID

    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO student (std_ID, Name, email, phone_no, Batch_year, LinkedIn_ID, LeetCode_ID) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                       (std_id, name, email, phone, batch, linkedin, leetcode))
        conn.commit()
        messagebox.showinfo("Success", f"Student added successfully with ID {std_id}!")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        conn.close()

# Function to fetch and display students
def fetch_students():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student")
    records = cursor.fetchall()
    conn.close()

    student_list.delete(0, tk.END)  # Clear listbox
    for record in records:
        student_list.insert(tk.END, record)

# Function to delete a student
def delete_student():
    selected_item = student_list.curselection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a student to delete")
        return

    std_id = student_list.get(selected_item)[0]  # Get std_ID from selected row

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM student WHERE std_ID=%s", (std_id,))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Student deleted successfully!")
    fetch_students()  # Refresh list

# GUI Design
root = tk.Tk()
root.title("Skill Edge Placement Hub")
root.geometry("500x500")

tk.Label(root, text="Student Name:").pack()
name_entry = tk.Entry(root)
name_entry.pack()

tk.Label(root, text="Student Email:").pack()
email_entry = tk.Entry(root)
email_entry.pack()

tk.Label(root, text="Phone Number:").pack()
phone_entry = tk.Entry(root)
phone_entry.pack()

tk.Label(root, text="Batch Year:").pack()
batch_entry = tk.Entry(root)
batch_entry.pack()

tk.Label(root, text="LinkedIn ID:").pack()
linkedin_entry = tk.Entry(root)
linkedin_entry.pack()

tk.Label(root, text="LeetCode ID:").pack()
leetcode_entry = tk.Entry(root)
leetcode_entry.pack()

tk.Button(root, text="Add Student", command=lambda: insert_student(
    name_entry.get(), email_entry.get(), phone_entry.get(), batch_entry.get(),
    linkedin_entry.get(), leetcode_entry.get())).pack()

tk.Label(root, text="Student List:").pack()
student_list = tk.Listbox(root, width=60)
student_list.pack()

tk.Button(root, text="Fetch Students", command=fetch_students).pack()
tk.Button(root, text="Delete Selected Student", command=delete_student).pack()

root.mainloop()
