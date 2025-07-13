import tkinter as tk
from db_connection import connect_db

def fetch_reports():
    conn = connect_db()
    cursor = conn.cursor()

    # Example Query: Count total students placed
    cursor.execute("SELECT COUNT(*) FROM placement")
    total_placements = cursor.fetchone()[0]

    # Example Query: Count total practice sessions
    cursor.execute("SELECT COUNT(*) FROM practice_section")
    total_practice_sessions = cursor.fetchone()[0]

    conn.close()

    report_label.config(text=f"Total Placements: {total_placements}\nTotal Practice Sessions: {total_practice_sessions}")

# Reports Management Window
def open_reports_management():
    global report_label

    report_window = tk.Toplevel()
    report_window.title("Reports & Analytics")

    tk.Button(report_window, text="Generate Reports", command=fetch_reports).pack()

    report_label = tk.Label(report_window, text="Click 'Generate Reports' to view stats", font=("Arial", 12))
    report_label.pack()
