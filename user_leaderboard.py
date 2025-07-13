import tkinter as tk
from tkinter import messagebox
from db_connection import connect_db

def view_leaderboard():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT student.Name, leaderboard.Points FROM leaderboard JOIN student ON leaderboard.Student_ID = student.std_ID ORDER BY Points DESC")
    rankings = cursor.fetchall()
    conn.close()

    leaderboard_text = "\n".join([f"{i+1}. {name} - {points} Points" for i, (name, points) in enumerate(rankings)])

    messagebox.showinfo("Leaderboard", leaderboard_text if leaderboard_text else "No leaderboard data available!")
