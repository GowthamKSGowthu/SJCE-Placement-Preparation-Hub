import tkinter as tk
from user_profile import view_profile
from user_practice import start_practice_test
from user_certifications import fetch_certifications
from user_resources import open_resources
from user_questions import open_questions
from user_answers import view_answers

def open_user_dashboard(root):
    user_window = tk.Toplevel(root)
    user_window.title("User Dashboard")
    user_window.geometry("600x500")
    user_window.configure(bg="#f0f5f9")  # Light background for better contrast

    # Header
    header_frame = tk.Frame(user_window, bg="#2c3e50", padx=20, pady=15)
    header_frame.pack(fill=tk.X)
    tk.Label(header_frame, text="User Dashboard", font=("Arial", 20, "bold"), bg="#2c3e50", fg="white").pack()

    # Main Content Frame
    main_frame = tk.Frame(user_window, bg="#f0f5f9")
    main_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

    # Sidebar-like Button Area
    btn_frame = tk.Frame(main_frame, bg="#ffffff", padx=20, pady=20, relief=tk.GROOVE, bd=3)
    btn_frame.pack(pady=10)

    # Button Styling & Functions
    def on_enter(event, btn):
        btn.config(bg="#1abc9c", fg="white")

    def on_leave(event, btn):
        btn.config(bg="#34495e", fg="white")

    buttons = [
        ("👤 View Profile", view_profile),
        ("📝 Start Practice Test", start_practice_test),
        ("🎓 View Certifications", fetch_certifications),
        ("📚 Access Study Resources", open_resources),
        ("❓ Attempt Questions", open_questions),
        ("✅ View Submitted Answers", view_answers),
        ("🚪 Logout", lambda: user_window.destroy())
    ]

    for text, command in buttons:
        btn = tk.Button(btn_frame, text=text, font=("Arial", 12, "bold"), bg="#34495e", fg="white",
                        padx=20, pady=7, relief=tk.RAISED, width=35, command=command)
        btn.pack(pady=8, padx=5)
        btn.bind("<Enter>", lambda e, b=btn: on_enter(e, b))
        btn.bind("<Leave>", lambda e, b=btn: on_leave(e, b))

    user_window.mainloop()
