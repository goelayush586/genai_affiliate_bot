import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("conversations.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history (
        username TEXT,
        message TEXT,
        response TEXT,
        feedback TEXT,
        timestamp TEXT
    )''')
    conn.commit()
    conn.close()

def log_conversation(username, message, response, feedback):
    conn = sqlite3.connect("conversations.db")
    c = conn.cursor()
    c.execute("INSERT INTO history VALUES (?, ?, ?, ?, ?)",
              (username, message, response, feedback, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def get_user_history(username):
    conn = sqlite3.connect("conversations.db")
    c = conn.cursor()
    c.execute("SELECT message, response, feedback, timestamp FROM history WHERE username=?", (username,))
    rows = c.fetchall()
    conn.close()
    return rows
