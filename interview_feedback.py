import tkinter as tk
from tkinter import messagebox
from db_connection import connect_db

# Function to fetch feedback
def fetch_feedback():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM interview_feedback")
    records = cursor.fetchall()
    conn.close()

    feedback_list.delete(0, tk.END)
    for record in records:
        feedback_list.insert(tk.END, record)

# Function to add feedback
def add_feedback():
    mock_id, feedback_text = mock_entry.get(), feedback_entry.get()

    if mock_id == "" or feedback_text == "":
        messagebox.showwarning("Warning", "Please enter all details")
        return

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO interview_feedback (mock_ID, feedback_text) VALUES (%s, %s)", 
                   (mock_id, feedback_text))
    conn.commit()
    conn.close()
    fetch_feedback()
    messagebox.showinfo("Success", "Feedback recorded successfully!")

# Interview Feedback Management Window
def open_interview_feedback():
    global mock_entry, feedback_entry, feedback_list

    feedback_window = tk.Toplevel()
    feedback_window.title("Interview Feedback Management")

    tk.Label(feedback_window, text="Mock Interview ID:").pack()
    mock_entry = tk.Entry(feedback_window)
    mock_entry.pack()

    tk.Label(feedback_window, text="Feedback:").pack()
    feedback_entry = tk.Entry(feedback_window)
    feedback_entry.pack()

    tk.Button(feedback_window, text="Add Feedback", command=add_feedback).pack()

    tk.Label(feedback_window, text="Feedback List:").pack()
    feedback_list = tk.Listbox(feedback_window, width=60)
    feedback_list.pack()

    tk.Button(feedback_window, text="Fetch Feedback", command=fetch_feedback).pack()

    fetch_feedback()
