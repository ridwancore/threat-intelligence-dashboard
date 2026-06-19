import sqlite3

DB_NAME = "threats.db"


def get_data(search=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    if search:
        cursor.execute("""
            SELECT * FROM indicators
            WHERE indicator LIKE ?
        """, ('%' + search + '%',))
    else:
        cursor.execute("SELECT * FROM indicators")

    rows = cursor.fetchall()
    conn.close()
    return rows


def init_db():
    conn = sqlite3.connect(DB_NAME)
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
    print("Database created successfully!")


# optional: run only when file executed directly
if __name__ == "__main__":
    init_db()