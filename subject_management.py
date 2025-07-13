import tkinter as tk
from tkinter import messagebox, ttk
from db_connection import connect_db

# Function to generate a unique subject ID
def generate_sub_id():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(Sub_ID) FROM subject")
    max_id = cursor.fetchone()[0]
    conn.close()
    return 1 if max_id is None else max_id + 1

# Function to fetch subjects
def fetch_subjects():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM subject")
    records = cursor.fetchall()
    conn.close()

    subject_list.delete(0, tk.END)
    for record in records:
        subject_list.insert(tk.END, f"{record[0]} - {record[1]} ({record[2]})")  # Displaying ID, Name, and Category

# Function to insert a subject
def insert_subject():
    sub_name, category = sub_name_entry.get().strip(), category_entry.get().strip()
    
    if sub_name == "" or category == "":
        messagebox.showwarning("Warning", "Please enter all details")
        return
    
    sub_id = generate_sub_id()
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO subject (Sub_ID, Sub_name, Category) VALUES (%s, %s, %s)", (sub_id, sub_name, category))
    conn.commit()
    conn.close()
    
    messagebox.showinfo("Success", "Subject added successfully!")
    sub_name_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    fetch_subjects()

# Function to delete a subject
def delete_subject():
    selected_item = subject_list.curselection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a subject to delete")
        return
    
    sub_id = subject_list.get(selected_item).split(" - ")[0]  # Extract Sub_ID
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM subject WHERE Sub_ID=%s", (sub_id,))
    conn.commit()
    conn.close()
    
    messagebox.showinfo("Success", "Subject deleted successfully!")
    fetch_subjects()

# Subject Management Window
def open_subject_management():
    global sub_name_entry, category_entry, subject_list

    sub_window = tk.Toplevel()
    sub_window.title("Manage Subjects")
    sub_window.geometry("500x450")
    sub_window.configure(bg="#e3f2fd")

    # Title Label
    tk.Label(sub_window, text="Subject Management", font=("Arial", 16, "bold"), bg="#e3f2fd", fg="#1a237e").pack(pady=10)

    # Frame for Input Fields
    input_frame = tk.Frame(sub_window, bg="#ffffff", padx=10, pady=10, relief=tk.GROOVE, bd=3)
    input_frame.pack(pady=10, fill="x", padx=20)

    tk.Label(input_frame, text="Subject Name:", font=("Arial", 12), bg="#ffffff").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    sub_name_entry = tk.Entry(input_frame, font=("Arial", 12), width=25)
    sub_name_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(input_frame, text="Category:", font=("Arial", 12), bg="#ffffff").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    category_entry = tk.Entry(input_frame, font=("Arial", 12), width=25)
    category_entry.grid(row=1, column=1, padx=5, pady=5)

    # Buttons Frame
    button_frame = tk.Frame(sub_window, bg="#e3f2fd")
    button_frame.pack(pady=5)

    # Button Hover Effects
    def on_enter(event, btn):
        btn.config(bg="#1b5e20", fg="white")

    def on_leave(event, btn):
        btn.config(bg="#388e3c", fg="white")

    add_button = tk.Button(button_frame, text="Add Subject", font=("Arial", 12, "bold"), bg="#388e3c", fg="white",
                           padx=15, pady=5, command=insert_subject)
    add_button.grid(row=0, column=0, padx=10, pady=5)
    add_button.bind("<Enter>", lambda event: on_enter(event, add_button))
    add_button.bind("<Leave>", lambda event: on_leave(event, add_button))

    fetch_button = tk.Button(button_frame, text="Fetch Subjects", font=("Arial", 12, "bold"), bg="#1976d2", fg="white",
                             padx=15, pady=5, command=fetch_subjects)
    fetch_button.grid(row=0, column=1, padx=10, pady=5)
    fetch_button.bind("<Enter>", lambda event: on_enter(event, fetch_button))
    fetch_button.bind("<Leave>", lambda event: on_leave(event, fetch_button))

    delete_button = tk.Button(button_frame, text="Delete Subject", font=("Arial", 12, "bold"), bg="#d32f2f", fg="white",
                              padx=15, pady=5, command=delete_subject)
    delete_button.grid(row=0, column=2, padx=10, pady=5)
    delete_button.bind("<Enter>", lambda event: on_enter(event, delete_button))
    delete_button.bind("<Leave>", lambda event: on_leave(event, delete_button))

    # Subject Listbox with Scrollbar
    list_frame = tk.Frame(sub_window, bg="#e3f2fd")
    list_frame.pack(pady=5, fill="both", expand=True, padx=20)

    tk.Label(list_frame, text="Subject List:", font=("Arial", 12, "bold"), bg="#e3f2fd").pack(anchor="w")

    scrollbar = tk.Scrollbar(list_frame)
    scrollbar.pack(side="right", fill="y")

    subject_list = tk.Listbox(list_frame, width=60, height=10, font=("Arial", 10), yscrollcommand=scrollbar.set)
    subject_list.pack(pady=5, fill="both", expand=True)
    scrollbar.config(command=subject_list.yview)

    fetch_subjects()  # Fetch subjects when the window opens
