import sqlite3

conn = sqlite3.connect("threats.db")
cursor = conn.cursor()

data = [
    ("192.168.1.1", "IP", 90, "DemoFeed"),
    ("malicious.com", "Domain", 85, "AbuseDB"),
    ("10.10.10.10", "IP", 70, "VirusTotal"),
    ("phishing-site.net", "Domain", 95, "PhishTank")
]

cursor.executemany(
    "INSERT INTO indicators (indicator, type, threat_score, source) VALUES (?, ?, ?, ?)",
    data
)

conn.commit()
conn.close()

print("Data added successfully!")