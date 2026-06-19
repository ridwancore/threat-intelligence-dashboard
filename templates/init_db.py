git import sqlite3

conn = sqlite3.connect("threats.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS indicators (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    indicator TEXT,
    type TEXT,
    threat_score INTEGER,
    source TEXT
)
""")

conn.commit()
conn.close()

print("Database initialized successfully!")