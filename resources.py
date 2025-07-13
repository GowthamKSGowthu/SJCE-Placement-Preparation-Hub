import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from db_connection import connect_db

def fetch_resources():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM resources")
    records = cursor.fetchall()
    conn.close()
    resource_list.delete(*resource_list.get_children())
    for record in records:
        resource_list.insert("", tk.END, values=record)

def add_resource():
    topic_id, resource_type, resource_link = topic_entry.get(), type_entry.get(), link_entry.get()
    if topic_id == "" or resource_type == "" or resource_link == "":
        messagebox.showwarning("Warning", "Please enter all details")
        return
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO resources (topic_ID, resource_type, resource_link) VALUES (%s, %s, %s)", 
                   (topic_id, resource_type, resource_link))
    conn.commit()
    conn.close()
    fetch_resources()
    messagebox.showinfo("Success", "Resource added successfully!")

def delete_resource():
    selected_item = resource_list.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a resource to delete")
        return
    resource_id = resource_list.item(selected_item)['values'][0]
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM resources WHERE Resources_ID=%s", (resource_id,))
    conn.commit()
    conn.close()
    fetch_resources()
    messagebox.showinfo("Success", "Resource deleted successfully!")

def open_resources():
    global topic_entry, type_entry, link_entry, resource_list
    resource_window = tk.Toplevel()
    resource_window.title("Manage Learning Resources")
    resource_window.geometry("700x500")
    resource_window.configure(bg="#f0f0f0")
    
    tk.Label(resource_window, text="Resource Management", font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#333").pack(pady=10)
    
    form_frame = tk.Frame(resource_window, bg="#ffffff", padx=10, pady=10, relief=tk.RIDGE, bd=2)
    form_frame.pack(pady=10)
    
    labels = ["Topic ID:", "Resource Type:", "Resource Link:"]
    entries = []
    for i, label in enumerate(labels):
        tk.Label(form_frame, text=label, font=("Arial", 10), bg="#ffffff").grid(row=i, column=0, pady=5, padx=10, sticky="w")
        entry = tk.Entry(form_frame, font=("Arial", 10))
        entry.grid(row=i, column=1, pady=5, padx=10)
        entries.append(entry)
    
    topic_entry, type_entry, link_entry = entries
    
    button_frame = tk.Frame(resource_window, bg="#f0f0f0")
    button_frame.pack()
    
    add_btn = tk.Button(button_frame, text="➕ Add Resource", font=("Arial", 12, "bold"), bg="#28a745", fg="white", padx=10, pady=5, command=add_resource)
    add_btn.grid(row=0, column=0, padx=10, pady=5)
    
    del_btn = tk.Button(button_frame, text="❌ Delete Resource", font=("Arial", 12, "bold"), bg="#dc3545", fg="white", padx=10, pady=5, command=delete_resource)
    del_btn.grid(row=0, column=1, padx=10, pady=5)
    
    refresh_btn = tk.Button(button_frame, text="🔄 Refresh", font=("Arial", 12, "bold"), bg="#007bff", fg="white", padx=10, pady=5, command=fetch_resources)
    refresh_btn.grid(row=0, column=2, padx=10, pady=5)
    
    resource_list = ttk.Treeview(resource_window, columns=("Resources ID", "Topic ID", "Resource Type", "Resource Link"), show="headings")
    resource_list.pack(pady=10, fill=tk.BOTH, expand=True)
    
    for col in ("Resources ID", "Topic ID", "Resource Type", "Resource Link"):
        resource_list.heading(col, text=col)
        resource_list.column(col, width=150, anchor="center")
    
    fetch_resources()
    resource_window.mainloop()
