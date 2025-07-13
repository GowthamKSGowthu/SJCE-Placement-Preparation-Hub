import tkinter as tk
from tkinter import messagebox
from db_connection import connect_db

def generate_cert_id():
    """Fetch the max Cert_ID from certification table and increment it"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(Cert_ID) FROM certification")
    max_id = cursor.fetchone()[0]
    conn.close()
    return 1 if max_id is None else max_id + 1

def fetch_certifications():
    global cert_list  # Declare global variable
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM certification")
    records = cursor.fetchall()
    conn.close()

    cert_list.delete(0, tk.END)  # Clear existing entries
    for record in records:
        cert_list.insert(tk.END, record)

def issue_certification():
    std_id = std_entry.get()
    cert_name = cert_entry.get()
    issued_by = issued_by_entry.get()
    issued_date = date_entry.get()

    if std_id == "" or cert_name == "" or issued_by == "" or issued_date == "":
        messagebox.showwarning("Warning", "Please enter all details")
        return

    cert_id = generate_cert_id()  # Generate new Cert_ID
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO certification (Cert_ID, Std_ID, Cert_name, Issued_by, Issued_date) VALUES (%s, %s, %s, %s, %s)", 
                   (cert_id, std_id, cert_name, issued_by, issued_date))
    conn.commit()
    conn.close()
    fetch_certifications()
    messagebox.showinfo("Success", f"Certification Issued Successfully with ID {cert_id}!")

def open_certification_management():
    global std_entry, cert_entry, issued_by_entry, date_entry, cert_list  # Declare global variables

    cert_window = tk.Toplevel()
    cert_window.title("Certification Management")
    cert_window.geometry("500x500")
    cert_window.configure(bg="#e3f2fd")

    tk.Label(cert_window, text="Certification Management", font=("Arial", 16, "bold"), bg="#42a5f5", fg="#ffffff", pady=10).pack(fill=tk.X)

    form_frame = tk.Frame(cert_window, bg="#ffffff", padx=10, pady=10, relief=tk.RIDGE, bd=2)
    form_frame.pack(pady=10)

    labels = ["Student ID:", "Certification Name:", "Issued By:", "Issued Date:"]
    entries = []
    for i, label in enumerate(labels):
        tk.Label(form_frame, text=label, font=("Arial", 10), bg="#ffffff").grid(row=i, column=0, pady=5, padx=10, sticky="w")
        entry = tk.Entry(form_frame, font=("Arial", 10))
        entry.grid(row=i, column=1, pady=5, padx=10)
        entries.append(entry)

    std_entry, cert_entry, issued_by_entry, date_entry = entries

    button_frame = tk.Frame(cert_window, bg="#e3f2fd")
    button_frame.pack()

    issue_btn = tk.Button(button_frame, text="🎓 Issue Certification", font=("Arial", 12, "bold"), bg="#66bb6a", fg="white", padx=10, pady=5, command=issue_certification)
    issue_btn.grid(row=0, column=0, padx=10, pady=5)

    fetch_btn = tk.Button(button_frame, text="🔄 Fetch Certifications", font=("Arial", 12, "bold"), bg="#29b6f6", fg="white", padx=10, pady=5, command=fetch_certifications)
    fetch_btn.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(cert_window, text="Certification List:", font=("Arial", 12, "bold"), bg="#e3f2fd").pack(pady=10)
    cert_list = tk.Listbox(cert_window, width=60, height=10)
    cert_list.pack()

    fetch_certifications()  # Fetch certifications on startup
