import json
import os
from datetime import datetime

LOG_PATH = "dashboard_logs.json"

def log_event(event_type, message):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    log_entry = {
        "time": timestamp,
        "type": event_type,
        "message": message
    }

    logs = []

    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []

    logs.append(log_entry)

    # Keep only last 100 logs to avoid huge file
    logs = logs[-100:]

    with open(LOG_PATH, "w") as f:
        json.dump(logs, f, indent=2)

    print(f"[{event_type.upper()}] {message}")
