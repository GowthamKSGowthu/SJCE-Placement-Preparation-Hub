import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Change if your username is different
        password="root",  # Replace with your MySQL password
        database="placementdb"
    )
