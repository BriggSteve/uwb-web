from flask import Flask, render_template, app
import psycopg2
import os


COMMAND_NAMES = {
    0: "POS_UPDATE",
    1: "HELLO_WORLD",
    2: "ALERT",
    3: "PING_REQUEST",
    4: "PING_RESPONSE",
    5: "SHUTDOWN",
    6: "CONFIG_UPDATE"
}


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

    # Convert command int to name
    packets = [
        (device_id, timestamp, x, y, z, COMMAND_NAMES.get(command, f"UNKNOWN ({command})"))
        for device_id, timestamp, x, y, z, command in rows
    ]
    return render_template("index.html", packets=packets)

if __name__ == "__main__":
    app.run(debug=True)
