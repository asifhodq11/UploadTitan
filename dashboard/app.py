from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

# This Flask app was created to show a dashboard log for the AI Comment Bot.
# It loads logs from 'dashboard_log.json' and shows them on a creative web interface.

LOG_FILE = "dashboard_log.json"

# Ensure log file exists
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        json.dump([], f)

@app.route("/")
def index():
    # Load recent log entries
    with open(LOG_FILE, "r") as f:
        logs = json.load(f)
    # Only show latest 20 entries
    logs = sorted(logs, key=lambda x: x.get("timestamp", ""), reverse=True)[:20]
    return render_template("index.html", logs=logs)

@app.route("/log", methods=["POST"])
def add_log():
    # Add new entry via POST (e.g., from main.py or bot)
    data = request.json
    with open(LOG_FILE, "r") as f:
        logs = json.load(f)
    logs.append(data)
    with open(LOG_FILE, "w") as f:
        json.dump(logs[-100:], f, indent=2)  # Keep last 100 logs
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(debug=True)
