import tkinter as tk
from tkinter import messagebox, ttk
from db_connection import connect_db

# Function to Submit Answers
def submit_answer(answers):
    conn = connect_db()
    cursor = conn.cursor()

    for question_id, answer_text in answers.items():
        if answer_text.strip():  # Ensure answer is not empty
            cursor.execute("INSERT INTO answers (Question_ID, Answer_text) VALUES (%s, %s)", (question_id, answer_text))

    conn.commit()
    conn.close()
    messagebox.showinfo("✅ Success", "Answers submitted successfully!")

# Function to View Submitted Answers
def view_answers():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT q.Question_text, a.Answer_text FROM answers a JOIN questions q ON a.Question_ID = q.Question_ID")
    records = cursor.fetchall()
    conn.close()

    if not records:
        messagebox.showinfo("❌ No Answers", "No answers available!")
        return

    # Create Answer Viewing Window
    answer_window = tk.Toplevel()
    answer_window.title("📄 View Submitted Answers")
    answer_window.geometry("600x500")
    answer_window.configure(bg="#f0f5f9")

    # Header Frame
    header_frame = tk.Frame(answer_window, bg="#2c3e50", padx=20, pady=10)
    header_frame.pack(fill=tk.X)
    tk.Label(header_frame, text="📌 Submitted Answers", font=("Arial", 16, "bold"), bg="#2c3e50", fg="white").pack()

    # Scrollable Frame
    container = tk.Frame(answer_window, bg="white", padx=20, pady=20, relief=tk.GROOVE, bd=3)
    container.pack(pady=10, fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(container, bg="white", highlightthickness=0)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="white")

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Display Questions & Answers
    for question, answer in records:
        answer_frame = tk.Frame(scrollable_frame, bg="#f8f9fa", padx=10, pady=10, relief=tk.GROOVE, bd=2)
        answer_frame.pack(pady=5, fill=tk.X, expand=True)
        
        tk.Label(answer_frame, text=f"❓ {question}", font=("Arial", 12, "bold"), bg="#f8f9fa", fg="#2c3e50", wraplength=500, justify="left").pack(anchor="w")
        tk.Label(answer_frame, text=f"✅ {answer}", font=("Arial", 12), bg="#f8f9fa", fg="#1b5e20").pack(anchor="w")

    # Hover Effects for Close Button
    def on_enter(event):
        close_button.config(bg="#d32f2f", fg="white")

    def on_leave(event):
        close_button.config(bg="#b71c1c", fg="white")

    # Close Button
    close_button = tk.Button(answer_window, text="❌ Close", font=("Arial", 12, "bold"), bg="#b71c1c", fg="white",
                             padx=20, pady=7, relief=tk.RAISED, command=answer_window.destroy)
    close_button.pack(pady=15)

    close_button.bind("<Enter>", on_enter)
    close_button.bind("<Leave>", on_leave)
