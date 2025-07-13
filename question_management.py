import tkinter as tk
from tkinter import messagebox
from db_connection import connect_db

# Function to generate a unique Question ID
def generate_question_id():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(Question_ID) FROM questions")
    max_id = cursor.fetchone()[0]
    conn.close()
    return 1 if max_id is None else max_id + 1

# Function to fetch questions
def fetch_questions():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions")
    records = cursor.fetchall()
    conn.close()

    question_list.delete(0, tk.END)
    for record in records:
        question_list.insert(tk.END, f"{record[0]} - {record[1]} ({record[2]}, {record[3]})")  # Displaying ID, Text, and Difficulty

# Function to insert a question
def insert_question():
    topic_id, question_text, difficulty = topic_entry.get().strip(), question_entry.get().strip(), difficulty_entry.get().strip()

    if not topic_id or not question_text or not difficulty:
        messagebox.showwarning("Warning", "Please enter all details")
        return
    
    question_id = generate_question_id()
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO questions (Question_ID, Topic_ID, Question_text, Difficulty_level) VALUES (%s, %s, %s, %s)", 
                   (question_id, topic_id, question_text, difficulty))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Question added successfully!")
    fetch_questions()

# Function to delete a question
def delete_question():
    selected_item = question_list.curselection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a question to delete")
        return
    
    question_id = question_list.get(selected_item).split(" - ")[0]  # Extract Question_ID
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM questions WHERE Question_ID=%s", (question_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Question deleted successfully!")
    fetch_questions()

# Question Management Window
def open_question_management():
    global topic_entry, question_entry, difficulty_entry, question_list

    question_window = tk.Toplevel()
    question_window.title("Manage Questions")
    question_window.geometry("500x400")
    question_window.configure(bg="#e3f2fd")

    tk.Label(question_window, text="Question Management", font=("Arial", 16, "bold"), bg="#e3f2fd", fg="#1a237e").pack(pady=10)

    tk.Label(question_window, text="Topic ID:", font=("Arial", 12), bg="#e3f2fd").pack()
    topic_entry = tk.Entry(question_window, font=("Arial", 12))
    topic_entry.pack()

    tk.Label(question_window, text="Question Text:", font=("Arial", 12), bg="#e3f2fd").pack()
    question_entry = tk.Entry(question_window, font=("Arial", 12))
    question_entry.pack()

    tk.Label(question_window, text="Difficulty Level:", font=("Arial", 12), bg="#e3f2fd").pack()
    difficulty_entry = tk.Entry(question_window, font=("Arial", 12))
    difficulty_entry.pack()

    button_frame = tk.Frame(question_window, bg="#e3f2fd")
    button_frame.pack(pady=5)

    tk.Button(button_frame, text="➕ Add Question", font=("Arial", 12, "bold"), bg="#388e3c", fg="white", command=insert_question).grid(row=0, column=0, padx=10, pady=5)
    tk.Button(button_frame, text="🔄 Fetch Questions", font=("Arial", 12, "bold"), bg="#1976d2", fg="white", command=fetch_questions).grid(row=0, column=1, padx=10, pady=5)
    tk.Button(button_frame, text="❌ Delete Question", font=("Arial", 12, "bold"), bg="#d32f2f", fg="white", command=delete_question).grid(row=0, column=2, padx=10, pady=5)

    tk.Label(question_window, text="Question List:", font=("Arial", 12, "bold"), bg="#e3f2fd").pack()
    
    list_frame = tk.Frame(question_window, bg="#e3f2fd")
    list_frame.pack(pady=5, fill="both", expand=True)

    scrollbar = tk.Scrollbar(list_frame)
    scrollbar.pack(side="right", fill="y")

    question_list = tk.Listbox(list_frame, width=60, height=10, font=("Arial", 10), yscrollcommand=scrollbar.set)
    question_list.pack(pady=5, fill="both", expand=True)
    scrollbar.config(command=question_list.yview)

    fetch_questions()