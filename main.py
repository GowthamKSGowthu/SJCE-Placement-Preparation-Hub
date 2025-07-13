import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from db_connection import connect_db
from admin_dashboard import open_admin_dashboard
from user_dashboard import open_user_dashboard

def login():
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if not username or not password:
        messagebox.showwarning("Login Failed", "Please enter both username and password!")
        return

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM user WHERE BINARY username=%s AND BINARY password=%s", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        role = user[0]
        messagebox.showinfo("Login Success", f"Welcome, {username}!")
        root.withdraw()

        if role == "admin":
            open_admin_dashboard(root)
        else:
            open_user_dashboard(root)
    else:
        messagebox.showerror("Login Failed", "Invalid username or password!")

# GUI Setup
root = tk.Tk()
root.title("Skill Edge Placement Hub - Login")
root.geometry("500x450")
root.configure(bg="#e3f2fd")
# Title
title_label = tk.Label(root, text="Skill Edge Placement Hub", font=("Arial", 18, "bold"), bg="#e3f2fd", fg="#1a237e")
title_label.pack(pady=15)
# Frame for Input Fields
frame = tk.Frame(root, bg="#ffffff", padx=25, pady=25, relief=tk.GROOVE, bd=3)
frame.pack(pady=15)

# Username Entry
tk.Label(frame, text="Username:", font=("Arial", 12), bg="#ffffff").grid(row=0, column=0, pady=8, padx=5, sticky="w")
username_entry = tk.Entry(frame, font=("Arial", 12))
username_entry.grid(row=0, column=1, pady=8, padx=5)

# Password Entry
tk.Label(frame, text="Password:", font=("Arial", 12), bg="#ffffff").grid(row=1, column=0, pady=8, padx=5, sticky="w")
password_entry = tk.Entry(frame, font=("Arial", 12), show="*")
password_entry.grid(row=1, column=1, pady=8, padx=5)

# Show/Hide Password Checkbox
def toggle_password():
    if password_var.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="*")

password_var = tk.BooleanVar()
toggle_button = tk.Checkbutton(frame, text="Show Password", variable=password_var, command=toggle_password, bg="#ffffff")
toggle_button.grid(row=2, columnspan=2, pady=5)

# Forgot Password Placeholder
def forgot_password():
    messagebox.showinfo("Forgot Password", "Password reset functionality coming soon!")

forgot_password_label = tk.Label(frame, text="Forgot Password?", font=("Arial", 10, "underline"), fg="#1a73e8", bg="#ffffff", cursor="hand2")
forgot_password_label.grid(row=3, columnspan=2, pady=5)
forgot_password_label.bind("<Button-1>", lambda e: forgot_password())

# Button Hover Effects
def on_enter(event):
    login_button.config(bg="#1b5e20", fg="white")

def on_leave(event):
    login_button.config(bg="#388e3c", fg="white")

# Login Button
login_button = tk.Button(root, text="Login", font=("Arial", 14, "bold"), bg="#388e3c", fg="white", padx=30, pady=10, relief=tk.RAISED, command=login)
login_button.pack(pady=15)
login_button.bind("<Enter>", on_enter)
login_button.bind("<Leave>", on_leave)

# Exit Button
def exit_app():
    root.destroy()

exit_button = tk.Button(root, text="Exit", font=("Arial", 12, "bold"), bg="#d32f2f", fg="white", padx=20, pady=5, relief=tk.RAISED, command=exit_app)
exit_button.pack(pady=5)

root.mainloop()
