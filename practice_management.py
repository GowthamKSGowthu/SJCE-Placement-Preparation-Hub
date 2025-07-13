import tkinter as tk
from tkinter import messagebox, ttk
from db_connection import connect_db

# Function to fetch practice sessions
def fetch_practice_sessions():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM practice_section")
    records = cursor.fetchall()
    conn.close()

    practice_table.delete(*practice_table.get_children())
    for record in records:
        practice_table.insert("", tk.END, values=record)

# Function to insert a practice session with manually generated Session_ID
def insert_practice():
    student_id, session_date, duration, problems_solved = student_entry.get(), date_entry.get(), duration_entry.get(), problems_entry.get()

    if not student_id or not session_date or not duration or not problems_solved:
        messagebox.showwarning("Warning", "Please enter all details!")
        return

    conn = connect_db()
    cursor = conn.cursor()

    # Generate next Session_ID manually
    cursor.execute("SELECT MAX(Session_ID) FROM practice_section")
    max_id = cursor.fetchone()[0]
    next_session_id = max_id + 1 if max_id else 1  # Start from 1 if no records exist

    try:
        cursor.execute("INSERT INTO practice_section (Session_ID, Student_ID, Session_date, Duration, Leetcode_problem_solved) VALUES (%s, %s, %s, %s, %s)", 
                       (next_session_id, student_id, session_date, duration, problems_solved))
        conn.commit()
        messagebox.showinfo("Success", "Practice session added successfully!")
        fetch_practice_sessions()
    except Exception as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
    finally:
        conn.close()

# Function to delete selected practice session
def delete_practice():
    selected_item = practice_table.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a session to delete!")
        return

    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this session?")
    if confirm:
        session_id = practice_table.item(selected_item, "values")[0]
        
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM practice_section WHERE Session_ID = %s", (session_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Deleted", "Practice session deleted successfully!")
        fetch_practice_sessions()

# Practice Management Window
def open_practice_management():
    global student_entry, date_entry, duration_entry, problems_entry, practice_table

    practice_window = tk.Toplevel()
    practice_window.title("Manage Practice Sessions")
    practice_window.geometry("700x500")
    practice_window.configure(bg="#e3f2fd")

    tk.Label(practice_window, text="Manage Practice Sessions", font=("Arial", 16, "bold"), bg="#e3f2fd", fg="#1a237e").pack(pady=10)

    form_frame = tk.Frame(practice_window, bg="#ffffff", padx=20, pady=15, relief=tk.GROOVE, bd=3)
    form_frame.pack(pady=10)

    # Input Fields
    tk.Label(form_frame, text="Student ID:", font=("Arial", 12), bg="#ffffff").grid(row=0, column=0, pady=5, padx=5, sticky="w")
    student_entry = tk.Entry(form_frame, font=("Arial", 12))
    student_entry.grid(row=0, column=1, pady=5, padx=5)

    tk.Label(form_frame, text="Session Date:", font=("Arial", 12), bg="#ffffff").grid(row=1, column=0, pady=5, padx=5, sticky="w")
    date_entry = tk.Entry(form_frame, font=("Arial", 12))
    date_entry.grid(row=1, column=1, pady=5, padx=5)

    tk.Label(form_frame, text="Duration:", font=("Arial", 12), bg="#ffffff").grid(row=2, column=0, pady=5, padx=5, sticky="w")
    duration_entry = tk.Entry(form_frame, font=("Arial", 12))
    duration_entry.grid(row=2, column=1, pady=5, padx=5)

    tk.Label(form_frame, text="Problems Solved:", font=("Arial", 12), bg="#ffffff").grid(row=3, column=0, pady=5, padx=5, sticky="w")
    problems_entry = tk.Entry(form_frame, font=("Arial", 12))
    problems_entry.grid(row=3, column=1, pady=5, padx=5)

    # Buttons
    btn_frame = tk.Frame(practice_window, bg="#e3f2fd")
    btn_frame.pack(pady=10)

    add_button = tk.Button(btn_frame, text="Add Session", font=("Arial", 12, "bold"), bg="#388e3c", fg="white", padx=20, command=insert_practice)
    add_button.grid(row=0, column=0, padx=10)

    fetch_button = tk.Button(btn_frame, text="Refresh Sessions", font=("Arial", 12, "bold"), bg="#1e88e5", fg="white", padx=20, command=fetch_practice_sessions)
    fetch_button.grid(row=0, column=1, padx=10)

    delete_button = tk.Button(btn_frame, text="Delete Session", font=("Arial", 12, "bold"), bg="#d32f2f", fg="white", padx=20, command=delete_practice)
    delete_button.grid(row=0, column=2, padx=10)

    # Practice Sessions Table
    table_frame = tk.Frame(practice_window, bg="#ffffff", padx=10, pady=10)
    table_frame.pack()

    columns = ("Session_ID", "Student_ID", "Session_date", "Duration", "Leetcode_problem_solved")
    practice_table = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

    for col in columns:
        practice_table.heading(col, text=col.replace("_", " "), anchor="center")
        practice_table.column(col, anchor="center", width=120)

    practice_table.pack()

    fetch_practice_sessions()
