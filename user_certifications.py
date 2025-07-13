import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageDraw, ImageFont
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from db_connection import connect_db

# Fetch Certifications from Database
def fetch_certifications():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT Cert_name, Issued_by, Issued_date FROM certification WHERE std_ID = 1")  # Replace with logged-in user ID
    records = cursor.fetchall()
    conn.close()

    if not records:
        messagebox.showinfo("Certifications", "No certifications found!")
        return

    # Open the certification display window
    display_certifications(records)

# Function to Generate Certificate as Image & PDF
def generate_certificate(user_name, cert_name, issued_by, issued_date):
    cert_filename = f"Certificate_{user_name.replace(' ', '_')}.pdf"
    
    # Create PDF Certificate
    c = canvas.Canvas(cert_filename, pagesize=letter)
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(300, 700, "Certificate of Achievement")

    c.setFont("Helvetica", 16)
    c.drawCentredString(300, 650, f"This is to certify that")
    
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(300, 620, user_name)

    c.setFont("Helvetica", 16)
    c.drawCentredString(300, 580, f"has successfully completed the")

    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(300, 550, cert_name)

    c.setFont("Helvetica", 14)
    c.drawCentredString(300, 520, f"Issued by: {issued_by}")

    c.setFont("Helvetica", 14)
    c.drawCentredString(300, 500, f"Issue Date: {issued_date}")

    c.setFont("Helvetica", 12)
    c.drawCentredString(300, 450, "Congratulations on your achievement!")

    c.showPage()
    c.save()

    messagebox.showinfo("Success", f"Certificate saved as {cert_filename}")

# Function to Display Certifications
def display_certifications(certificates):
    cert_window = tk.Toplevel()
    cert_window.title("Your Certifications")
    cert_window.geometry("500x400")
    cert_window.configure(bg="#f0f5f9")

    # Header
    header_frame = tk.Frame(cert_window, bg="#2c3e50", padx=20, pady=10)
    header_frame.pack(fill=tk.X)
    tk.Label(header_frame, text="🎓 Your Certifications", font=("Arial", 16, "bold"), bg="#2c3e50", fg="white").pack()

    # Scrollable Frame
    container = tk.Frame(cert_window, bg="#f0f5f9")
    canvas = tk.Canvas(container, bg="#f0f5f9", highlightthickness=0)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="white", padx=20, pady=20)

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    container.pack(fill="both", expand=True, pady=10)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Entry Field for User Name
    tk.Label(scrollable_frame, text="Enter Your Name:", font=("Arial", 12, "bold"), bg="white").pack(pady=5)
    name_entry = tk.Entry(scrollable_frame, font=("Arial", 12), width=30)
    name_entry.pack(pady=5)

    for cert in certificates:
        cert_frame = tk.Frame(scrollable_frame, bg="#ffffff", padx=10, pady=10, relief=tk.GROOVE, bd=2)
        cert_frame.pack(pady=5, fill=tk.X, expand=True)
        tk.Label(cert_frame, text=f"📜 {cert[0]}", font=("Arial", 12, "bold"), bg="white", fg="#2c3e50").pack(anchor="w")
        tk.Label(cert_frame, text=f"🏛 Issued by: {cert[1]}", font=("Arial", 10), bg="white", fg="#555").pack(anchor="w")
        tk.Label(cert_frame, text=f"📅 Date: {cert[2]}", font=("Arial", 10), bg="white", fg="#555").pack(anchor="w")

        generate_button = tk.Button(cert_frame, text="📄 Generate Certificate", font=("Arial", 10, "bold"), bg="#388e3c", fg="white",
                                    padx=10, pady=5, relief=tk.RAISED, command=lambda c=cert: generate_certificate(name_entry.get(), c[0], c[1], c[2]))
        generate_button.pack(pady=5)

    # Close Button with Hover Effect
    def on_enter(event):
        close_button.config(bg="#d32f2f", fg="white")

    def on_leave(event):
        close_button.config(bg="#b71c1c", fg="white")

    close_button = tk.Button(cert_window, text="❌ Close", font=("Arial", 12, "bold"), bg="#b71c1c", fg="white",
                             padx=20, pady=7, relief=tk.RAISED, command=cert_window.destroy)
    close_button.pack(pady=15)

    close_button.bind("<Enter>", on_enter)
    close_button.bind("<Leave>", on_leave)
