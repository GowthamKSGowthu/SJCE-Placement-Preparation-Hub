import tkinter as tk
from tkinter import messagebox
import webbrowser
import pyperclip  # For copying links to clipboard
from db_connection import connect_db

# Function to fetch study resources
def open_resources():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT Resource_type, Resource_link FROM resources")
    resources = cursor.fetchall()
    conn.close()

    if not resources:
        messagebox.showinfo("Resources", "No resources available!")
        return

    # Create Window
    resources_window = tk.Toplevel()
    resources_window.title("📚 Study Resources")
    resources_window.geometry("500x400")
    resources_window.configure(bg="#f0f5f9")

    # Header
    header_frame = tk.Frame(resources_window, bg="#2c3e50", padx=20, pady=10)
    header_frame.pack(fill=tk.X)
    tk.Label(header_frame, text="📖 Available Study Resources", font=("Arial", 16, "bold"), bg="#2c3e50", fg="white").pack()

    # Container Frame
    container = tk.Frame(resources_window, bg="white", padx=20, pady=20, relief=tk.GROOVE, bd=3)
    container.pack(pady=10, fill=tk.BOTH, expand=True)

    def open_link(link):
        webbrowser.open(link)

    def copy_link(link):
        pyperclip.copy(link)
        messagebox.showinfo("Copied", "Resource link copied to clipboard!")

    # Display Resources with Buttons
    for r_type, link in resources:
        resource_frame = tk.Frame(container, bg="#ffffff", padx=10, pady=5, relief=tk.GROOVE, bd=2)
        resource_frame.pack(pady=5, fill=tk.X, expand=True)

        tk.Label(resource_frame, text=f"📌 {r_type}", font=("Arial", 12, "bold"), bg="white", fg="#2c3e50").pack(anchor="w")
        
        btn_frame = tk.Frame(resource_frame, bg="white")
        btn_frame.pack(anchor="w", pady=5)

        open_button = tk.Button(btn_frame, text="🌐 Open", font=("Arial", 10, "bold"), bg="#388e3c", fg="white",
                                padx=10, pady=5, relief=tk.RAISED, command=lambda l=link: open_link(l))
        open_button.grid(row=0, column=0, padx=5)

        copy_button = tk.Button(btn_frame, text="📋 Copy Link", font=("Arial", 10, "bold"), bg="#1e88e5", fg="white",
                                padx=10, pady=5, relief=tk.RAISED, command=lambda l=link: copy_link(l))
        copy_button.grid(row=0, column=1, padx=5)

    # Close Button with Hover Effect
    def on_enter(event):
        close_button.config(bg="#d32f2f", fg="white")

    def on_leave(event):
        close_button.config(bg="#b71c1c", fg="white")

    close_button = tk.Button(resources_window, text="❌ Close", font=("Arial", 12, "bold"), bg="#b71c1c", fg="white",
                             padx=20, pady=7, relief=tk.RAISED, command=resources_window.destroy)
    close_button.pack(pady=15)

    close_button.bind("<Enter>", on_enter)
    close_button.bind("<Leave>", on_leave)
