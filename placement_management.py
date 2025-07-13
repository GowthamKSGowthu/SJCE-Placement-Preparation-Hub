import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from db_connection import connect_db

def generate_placement_id():
    """Fetch the max Placement_ID from placement table and increment it"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(Placement_ID) FROM placement")
    max_id = cursor.fetchone()[0]
    conn.close()
    return 1 if max_id is None else max_id + 1

def fetch_placements():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM placement")
    records = cursor.fetchall()
    conn.close()
    placement_list.delete(*placement_list.get_children())
    for record in records:
        placement_list.insert("", tk.END, values=record)

def insert_placement():
    std_id, company_id, date = std_entry.get(), company_entry.get(), date_entry.get()
    if std_id == "" or company_id == "" or date == "":
        messagebox.showwarning("Warning", "Please enter all details")
        return

    placement_id = generate_placement_id()  # Generate new Placement_ID
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO placement (Placement_ID, Std_ID, Company_ID, Placement_Date) VALUES (%s, %s, %s, %s)", 
                   (placement_id, std_id, company_id, date))
    conn.commit()
    conn.close()
    fetch_placements()
    messagebox.showinfo("Success", f"Placement added successfully with ID {placement_id}!")

def delete_placement():
    selected_item = placement_list.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a placement to delete")
        return
    placement_id = placement_list.item(selected_item)['values'][0]
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM placement WHERE Placement_ID=%s", (placement_id,))
    conn.commit()
    conn.close()
    fetch_placements()
    messagebox.showinfo("Success", "Placement deleted successfully!")

def open_placement_management():
    global std_entry, company_entry, date_entry, placement_list
    placement_window = tk.Toplevel()
    placement_window.title("Placement Management")
    placement_window.geometry("750x550")
    placement_window.configure(bg="#e3f2fd")
    
    tk.Label(placement_window, text="Placement Management", font=("Arial", 18, "bold"), bg="#42a5f5", fg="#ffffff", pady=10).pack(fill=tk.X)
    
    form_frame = tk.Frame(placement_window, bg="#ffffff", padx=15, pady=15, relief=tk.RIDGE, bd=2)
    form_frame.pack(pady=10)
    
    labels = ["Student ID:", "Company ID:", "Placement Date:"]
    entries = []
    for i, label in enumerate(labels):
        tk.Label(form_frame, text=label, font=("Arial", 12), bg="#ffffff").grid(row=i, column=0, pady=5, padx=10, sticky="w")
        entry = tk.Entry(form_frame, font=("Arial", 12))
        entry.grid(row=i, column=1, pady=5, padx=10)
        entries.append(entry)
    
    std_entry, company_entry, date_entry = entries
    
    button_frame = tk.Frame(placement_window, bg="#e3f2fd")
    button_frame.pack(pady=10)
    
    add_btn = tk.Button(button_frame, text="➕ Add", font=("Arial", 12, "bold"), bg="#66bb6a", fg="white", padx=12, pady=6, command=insert_placement)
    add_btn.grid(row=0, column=0, padx=10, pady=5)
    
    del_btn = tk.Button(button_frame, text="❌ Delete", font=("Arial", 12, "bold"), bg="#ef5350", fg="white", padx=12, pady=6, command=delete_placement)
    del_btn.grid(row=0, column=1, padx=10, pady=5)
    
    refresh_btn = tk.Button(button_frame, text="🔄 Refresh", font=("Arial", 12, "bold"), bg="#29b6f6", fg="white", padx=12, pady=6, command=fetch_placements)
    refresh_btn.grid(row=0, column=2, padx=10, pady=5)
    
    placement_list = ttk.Treeview(placement_window, columns=("Placement ID", "Student ID", "Company ID", "Placement Date"), show="headings")
    placement_list.pack(pady=10, fill=tk.BOTH, expand=True)
    
    for col in ("Placement ID", "Student ID", "Company ID", "Placement Date"):
        placement_list.heading(col, text=col)
        placement_list.column(col, width=150, anchor="center")
    
    fetch_placements()
    placement_window.mainloop()