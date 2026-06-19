from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


def db():
    conn = sqlite3.connect("threats.db")
    return conn


def init():
    conn = db()
    cur = conn.cursor()
    cur.execute("""
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

init()


@app.route("/")
def home():
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM indicators")
    data = cur.fetchall()
    conn.close()

    high = sum(1 for r in data if r[3] >= 80)
    medium = sum(1 for r in data if 50 <= r[3] < 80)
    low = sum(1 for r in data if r[3] < 50)

    return render_template(
        "index.html",
        data=data,
        high=high,
        medium=medium,
        low=low
    )


@app.route("/add", methods=["POST"])
def add():
    indicator = request.form["indicator"]
    type_ = request.form["type"]
    score = int(request.form["score"])
    source = request.form["source"]

    conn = db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO indicators (indicator, type, threat_score, source)
        VALUES (?, ?, ?, ?)
    """, (indicator, type_, score, source))

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/delete/<int:id>")
def delete(id):
    conn = db()
    cur = conn.cursor()
    cur.execute("DELETE FROM indicators WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")


@app.route("/search")
def search():
    q = request.args.get("q")

    conn = db()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM indicators
        WHERE indicator LIKE ? OR type LIKE ? OR source LIKE ?
    """, (f"%{q}%", f"%{q}%", f"%{q}%"))

    data = cur.fetchall()
    conn.close()

    return render_template("index.html", data=data, high=0, medium=0, low=0)


if __name__ == "__main__":
    app.run(debug=True)