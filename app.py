from flask import Flask, render_template
import psycopg2
import os

app = Flask(__name__)

# Read DB credentials from environment
conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT", 5432)
)

@app.route("/")
def index():
    cur = conn.cursor()
    cur.execute("""
        SELECT device_id, timestamp, x, y, z, command
        FROM packets
        ORDER BY timestamp DESC
        LIMIT 20
    """)

    rows = cur.fetchall()
    cur.close()
    return render_template("index.html", packets=rows)

if __name__ == "__main__":
    app.run(debug=True)
