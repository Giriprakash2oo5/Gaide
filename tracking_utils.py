import sqlite3
from datetime import datetime

DB_FILE = "learner_tracking.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS performance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            subject TEXT,
            lesson TEXT,
            attempt_number INTEGER,
            score INTEGER,
            total_questions INTEGER,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_performance(user, subject, lesson, attempt_number, score, total_questions):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO performance (user, subject, lesson, attempt_number, score, total_questions, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (user, subject, lesson, attempt_number, score, total_questions, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def get_user_performance(user, subject):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT attempt_number, score, total_questions, timestamp
        FROM performance
        WHERE user = ? AND subject = ?
        ORDER BY attempt_number ASC
    """, (user, subject))
    data = cursor.fetchall()
    conn.close()
    return data
