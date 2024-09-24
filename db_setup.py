import sqlite3
from datetime import datetime, timedelta

def create_tables():
    conn = sqlite3.connect('sun_lab_access.db')
    c = conn.cursor()

    # Create table for access logs
    c.execute('''CREATE TABLE IF NOT EXISTS access_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER NOT NULL,
                    timestamp TEXT NOT NULL
                 )''')

    # Create table for users
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER NOT NULL UNIQUE,
                    user_type TEXT NOT NULL,
                    status TEXT NOT NULL CHECK(status IN ('active', 'suspended', 'reactivated'))
                 )''')

    # Delete any existing data for a clean start
    c.execute("DELETE FROM access_logs")
    c.execute("DELETE FROM users")

    # Add dummy data for users
    c.execute("INSERT INTO users (student_id, user_type, status) VALUES (?, ?, ?)", (12345, 'student', 'active'))
    c.execute("INSERT INTO users (student_id, user_type, status) VALUES (?, ?, ?)", (67890, 'faculty', 'active'))
    c.execute("INSERT INTO users (student_id, user_type, status) VALUES (?, ?, ?)", (11111, 'student', 'active'))
    c.execute("INSERT INTO users (student_id, user_type, status) VALUES (?, ?, ?)", (22222, 'student', 'suspended'))
    c.execute("INSERT INTO users (student_id, user_type, status) VALUES (?, ?, ?)", (33333, 'staff', 'active'))

    # Add multiple logs with different timestamps for testing
    now = datetime.now()

    logs = [
        (12345, now.strftime("%Y-%m-%d %H:%M:%S")),
        (67890, now.strftime("%Y-%m-%d %H:%M:%S")),
        (11111, (now - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")),
        (22222, (now - timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S")),
        (33333, (now - timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S")),
        (12345, (now - timedelta(days=4)).strftime("%Y-%m-%d %H:%M:%S")),
        (67890, (now - timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S")),
    ]

    c.executemany("INSERT INTO access_logs (student_id, timestamp) VALUES (?, ?)", logs)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
