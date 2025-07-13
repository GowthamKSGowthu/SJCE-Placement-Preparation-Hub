import tkinter as tk
import time
from student_management import open_student_management
from placement_management import open_placement_management
from certification_management import open_certification_management
from resources import open_resources
from subject_management import open_subject_management
from question_management import open_question_management
from practice_management import open_practice_management

# Function for fade-in effect on welcome label
def fade_in_label(label):
    for i in range(1, 11):
        label.config(fg="#1c2833")  # Darker text effect
        label.update()
        time.sleep(0.1)

# Function to open Admin Dashboard
def open_admin_dashboard(root):
    admin_window = tk.Toplevel(root)
    admin_window.title("Admin Dashboard")
    admin_window.geometry("800x600")
    admin_window.configure(bg="#f8f9fa")  # Light Background

    # Header
    header_frame = tk.Frame(admin_window, bg="#154360", padx=20, pady=15)
    header_frame.pack(fill=tk.X)
    tk.Label(header_frame, text="Admin Dashboard", font=("Arial", 20, "bold"), bg="#154360", fg="white").pack()

    # Content Area
    content_frame = tk.Frame(admin_window, bg="#f8f9fa")
    content_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

    # Sidebar
    sidebar = tk.Frame(content_frame, bg="#1b2631", width=250, relief=tk.RIDGE, bd=3)
    sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

    # Main Content Area
    main_area = tk.Frame(content_frame, bg="white", padx=20, pady=20, relief=tk.GROOVE, bd=3)
    main_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # Sidebar Buttons Data
    buttons = [
        ("📚 Manage Students", open_student_management),
        ("🏢 Manage Placements", open_placement_management),
        ("🎓 Manage Certifications", open_certification_management),
        ("📂 Manage Resources", open_resources),
        ("📖 Manage Subjects & Topics", open_subject_management),
        ("❓ Manage Questions & Answers", open_question_management),
        ("📝 Manage Practice Sessions", open_practice_management),
        ("🚪 Logout", lambda: admin_window.destroy())
    ]

    # Sidebar Button Hover Effects
    def on_enter(event, btn):
        btn.config(bg="#2471A3", fg="white", font=("Arial", 13, "bold"), relief=tk.SUNKEN)

    def on_leave(event, btn):
        btn.config(bg="#1b2631", fg="white", font=("Arial", 12, "bold"), relief=tk.RAISED)

    # Create Sidebar Buttons
    for text, command in buttons:
        btn = tk.Button(sidebar, text=text, font=("Arial", 12, "bold"), bg="#1b2631", fg="white",
                        padx=10, pady=7, relief=tk.RAISED, width=30, command=command)
        btn.pack(pady=8, padx=5)
        btn.bind("<Enter>", lambda e, b=btn: on_enter(e, b))
        btn.bind("<Leave>", lambda e, b=btn: on_leave(e, b))

    # Welcome Message
    welcome_label = tk.Label(main_area, text="✨ Welcome to the Admin Dashboard! ✨", font=("Arial", 18, "bold"),
                             bg="white", fg="#1c2833")
    welcome_label.pack(pady=20)
    fade_in_label(welcome_label)

    admin_window.mainloop()
