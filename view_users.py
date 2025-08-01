# view_users.py
import sqlite3

DB = "data/database.db"

with sqlite3.connect(DB) as conn:
    users = conn.execute("SELECT id, username FROM users").fetchall()
    for u in users:
        print(u)
