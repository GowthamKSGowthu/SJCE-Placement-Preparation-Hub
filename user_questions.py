import tkinter as tk
from tkinter import messagebox, ttk
from db_connection import connect_db
from user_answers import submit_answer

# Fetch Questions from Database
def fetch_questions():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT Question_ID, Question_text FROM questions LIMIT 5")  # Fetch 5 random questions
    questions = cursor.fetchall()
    conn.close()
    return questions

# Open Question Attempt Window
def open_questions():
    question_window = tk.Toplevel()
    question_window.title("📝 Attempt Questions")
    question_window.geometry("600x500")
    question_window.configure(bg="#f0f5f9")

    # Header
    header_frame = tk.Frame(question_window, bg="#2c3e50", padx=20, pady=10)
    header_frame.pack(fill=tk.X)
    tk.Label(header_frame, text="📝 Answer the Questions Below", font=("Arial", 16, "bold"), bg="#2c3e50", fg="white").pack()

    # Scrollable Frame
    container = tk.Frame(question_window, bg="white", padx=20, pady=20, relief=tk.GROOVE, bd=3)
    container.pack(pady=10, fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(container, bg="white", highlightthickness=0)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="white")

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Fetch Questions
    questions = fetch_questions()
    
    if not questions:
        messagebox.showinfo("Questions", "No questions available!")
        question_window.destroy()
        return

    answer_entries = {}

    for q_id, text in questions:
        question_frame = tk.Frame(scrollable_frame, bg="#f8f9fa", padx=10, pady=10, relief=tk.GROOVE, bd=2)
        question_frame.pack(pady=5, fill=tk.X, expand=True)
        
        tk.Label(question_frame, text=f"❓ {text}", font=("Arial", 12, "bold"), bg="#f8f9fa", fg="#2c3e50", wraplength=500, justify="left").pack(anchor="w")
        
        entry = tk.Entry(question_frame, font=("Arial", 12), width=55, relief=tk.SOLID, bd=2)
        entry.pack(pady=5)
        answer_entries[q_id] = entry

    # Hover Effects for Buttons
    def on_enter(event, btn):
        btn.config(bg="#1abc9c", fg="white")

    def on_leave(event, btn):
        btn.config(bg="#34495e", fg="white")

    # Submit Answers
    def submit():
        answers = {q_id: entry.get() for q_id, entry in answer_entries.items()}
        submit_answer(answers)
        messagebox.showinfo("✅ Submitted", "Your answers have been recorded!")

    submit_button = tk.Button(question_window, text="📤 Submit Answers", font=("Arial", 14, "bold"), bg="#34495e", fg="white",
                              padx=20, pady=10, relief=tk.RAISED, command=submit)
    submit_button.pack(pady=20)

    submit_button.bind("<Enter>", lambda e: on_enter(e, submit_button))
    submit_button.bind("<Leave>", lambda e: on_leave(e, submit_button))
