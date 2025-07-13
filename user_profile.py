import tkinter as tk
from tkinter import messagebox
from db_connection import connect_db

# Function to View Profile
def view_profile():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT Name, email, phone_no, LinkedIn_ID, LeetCode_ID FROM student WHERE std_ID = 1")  # Replace with logged-in user ID
    profile_data = cursor.fetchone()
    conn.close()

    if profile_data:
        profile_info = (
            f"👤 Name: {profile_data[0]}\n"
            f"📧 Email: {profile_data[1]}\n"
            f"📞 Phone: {profile_data[2]}\n"
            f"🔗 LinkedIn: {profile_data[3]}\n"
            f"💻 LeetCode: {profile_data[4]}"
        )
        messagebox.showinfo("Profile Information", profile_info)
    else:
        messagebox.showerror("Error", "Profile not found!")

# Function to Open Edit Profile Window
def open_edit_profile():
    edit_window = tk.Toplevel()
    edit_window.title("Edit Profile")
    edit_window.geometry("400x300")
    edit_window.configure(bg="#f0f5f9")  # Light background for a modern feel

    tk.Label(edit_window, text="Update Your Details", font=("Arial", 14, "bold"), bg="#f0f5f9", fg="#2c3e50").pack(pady=10)

    form_frame = tk.Frame(edit_window, bg="#ffffff", padx=20, pady=20, relief=tk.GROOVE, bd=3)
    form_frame.pack(pady=10)

    # Labels and Entry Fields
    tk.Label(form_frame, text="📧 Email:", font=("Arial", 12), bg="#ffffff").grid(row=0, column=0, pady=5, padx=5, sticky="w")
    email_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
    email_entry.grid(row=0, column=1, pady=5, padx=5)

    tk.Label(form_frame, text="📞 Phone:", font=("Arial", 12), bg="#ffffff").grid(row=1, column=0, pady=5, padx=5, sticky="w")
    phone_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
    phone_entry.grid(row=1, column=1, pady=5, padx=5)

    tk.Label(form_frame, text="🔗 LinkedIn:", font=("Arial", 12), bg="#ffffff").grid(row=2, column=0, pady=5, padx=5, sticky="w")
    linkedin_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
    linkedin_entry.grid(row=2, column=1, pady=5, padx=5)

    tk.Label(form_frame, text="💻 LeetCode:", font=("Arial", 12), bg="#ffffff").grid(row=3, column=0, pady=5, padx=5, sticky="w")
    leetcode_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
    leetcode_entry.grid(row=3, column=1, pady=5, padx=5)

    # Button Hover Effects
    def on_enter(event, btn):
        btn.config(bg="#1abc9c", fg="white")

    def on_leave(event, btn):
        btn.config(bg="#34495e", fg="white")

    # Save Changes Button
    save_button = tk.Button(edit_window, text="💾 Save Changes", font=("Arial", 12, "bold"), bg="#34495e", fg="white",
                            padx=20, pady=8, relief=tk.RAISED, command=lambda: update_profile(
                                email_entry.get(), phone_entry.get(), linkedin_entry.get(), leetcode_entry.get()))
    save_button.pack(pady=15)

    save_button.bind("<Enter>", lambda e: on_enter(e, save_button))
    save_button.bind("<Leave>", lambda e: on_leave(e, save_button))

# Function to Update Profile in Database
def update_profile(email, phone, linkedin, leetcode):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE student SET email=%s, phone_no=%s, LinkedIn_ID=%s, LeetCode_ID=%s WHERE std_ID=1", (email, phone, linkedin, leetcode))  # Replace with logged-in user ID
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Profile updated successfully!")
