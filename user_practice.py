import tkinter as tk
from tkinter import messagebox, ttk
from db_connection import connect_db

# Fetch available topics
def fetch_topics():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT Topic_ID, Topic_name FROM topic")
    topics = cursor.fetchall()
    conn.close()
    return topics

# Fetch questions based on Topic & Difficulty
def fetch_questions(topic_id, difficulty):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT Question_ID, Question_text FROM questions WHERE Topic_ID = %s AND Difficulty_level = %s", (topic_id, difficulty))
    questions = cursor.fetchall()
    conn.close()
    return questions

# Open Practice Test Window
def start_practice_test():
    topic_window = tk.Toplevel()
    topic_window.title("Select Topic & Difficulty")
    topic_window.geometry("500x400")
    topic_window.configure(bg="#f0f5f9")

    # Center Frame
    center_frame = tk.Frame(topic_window, bg="white", padx=30, pady=30, relief=tk.GROOVE, bd=3)
    center_frame.pack(expand=True)

    tk.Label(center_frame, text="📘 Select a Topic", font=("Arial", 14, "bold"), bg="white", fg="#2c3e50").pack(pady=8)

    topics = fetch_topics()
    
    if not topics:
        messagebox.showinfo("No Topics", "No topics available!")
        topic_window.destroy()
        return

    topic_var = tk.StringVar(topic_window)
    topic_dropdown = ttk.Combobox(center_frame, textvariable=topic_var, values=[f"{t[0]} - {t[1]}" for t in topics], state="readonly", font=("Arial", 12))
    topic_dropdown.pack(pady=5)
    topic_dropdown.current(0)

    tk.Label(center_frame, text="🎯 Select Difficulty Level", font=("Arial", 14, "bold"), bg="white", fg="#2c3e50").pack(pady=8)

    difficulty_var = tk.StringVar(topic_window)
    difficulty_dropdown = ttk.Combobox(center_frame, textvariable=difficulty_var, values=["1", "2", "3", "4"], state="readonly", font=("Arial", 12))
    difficulty_dropdown.pack(pady=5)
    difficulty_dropdown.current(0)

    def on_enter(event, btn):
        btn.config(bg="#1abc9c", fg="white")

    def on_leave(event, btn):
        btn.config(bg="#34495e", fg="white")

    def load_questions():
        topic_id = topic_var.get().split(" - ")[0]
        difficulty = difficulty_var.get()
        display_questions(topic_id, difficulty)

    start_button = tk.Button(center_frame, text="🚀 Start Test", font=("Arial", 12, "bold"), bg="#34495e", fg="white",
                             padx=20, pady=8, relief=tk.RAISED, command=load_questions)
    start_button.pack(pady=15)
    start_button.bind("<Enter>", lambda e: on_enter(e, start_button))
    start_button.bind("<Leave>", lambda e: on_leave(e, start_button))

# Display Questions with Centered Frames & Scrollable View
def display_questions(topic_id, difficulty):
    question_window = tk.Toplevel()
    question_window.title(f"Practice Test - Difficulty {difficulty}")
    question_window.geometry("600x500")
    question_window.configure(bg="#f8f9fa")

    # Centered Container
    container = tk.Frame(question_window, bg="#f8f9fa", padx=10, pady=10)
    container.pack(fill="both", expand=True)

    # Scrollable Canvas
    canvas = tk.Canvas(container, width=580, bg="#f8f9fa", highlightthickness=0)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="white", padx=30, pady=20, relief=tk.GROOVE, bd=3)

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    tk.Label(scrollable_frame, text=f"📝 Questions - Difficulty {difficulty}", font=("Arial", 16, "bold"), bg="white", fg="#2c3e50").pack(pady=10)

    questions = fetch_questions(topic_id, difficulty)

    if not questions:
        messagebox.showinfo("No Questions", f"No difficulty {difficulty} questions available for this topic!")
        question_window.destroy()
        return

    answer_entries = {}

    def animate_entry(entry):
        entry.config(bg="#e3f2fd")  # Light blue when focused
        entry.after(1000, lambda: entry.config(bg="white"))  # Restore after 1 sec

    for q_id, text in questions:
        tk.Label(scrollable_frame, text=text, font=("Arial", 12), wraplength=500, justify="left", bg="white", fg="#2c3e50").pack(pady=5)
        entry = tk.Entry(scrollable_frame, font=("Arial", 12), width=55, relief=tk.SOLID, bd=2)
        entry.pack(pady=5)
        entry.bind("<FocusIn>", lambda e, ent=entry: animate_entry(ent))  # Animation on focus
        answer_entries[q_id] = entry

    def submit():
        answers = {q_id: entry.get() for q_id, entry in answer_entries.items()}
        messagebox.showinfo("✅ Test Submitted", "Your answers have been recorded!")

    submit_button = tk.Button(scrollable_frame, text="📤 Submit Answers", font=("Arial", 14, "bold"), bg="#34495e", fg="white",
                              padx=20, pady=10, relief=tk.RAISED, command=submit)
    submit_button.pack(pady=20)

    submit_button.bind("<Enter>", lambda e: on_enter(e, submit_button))
    submit_button.bind("<Leave>", lambda e: on_leave(e, submit_button))
