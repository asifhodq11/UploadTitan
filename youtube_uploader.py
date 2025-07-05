import os
import json
import time
import logging
import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from youtube_scheduler import get_best_upload_time
from dashboard_logger import send_log

RETRIES = 3
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
HISTORY_FILE = ".upload_history.json"

def load_upload_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return {}

def save_upload_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)

def upload_video(video_path, title, description, tags):
    creds = Credentials.from_authorized_user_file("youtube_token.json", SCOPES)
    youtube = build("youtube", "v3", credentials=creds)
    upload_time = get_best_upload_time()
    upload_dt = datetime.datetime.fromtimestamp(upload_time)

    logging.info(f"Scheduling upload at {upload_dt}")

    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "24"  # "Entertainment"
        },
        "status": {
            "privacyStatus": "private",
            "publishAt": upload_dt.isoformat() + "Z",
            "selfDeclaredMadeForKids": False
        }
    }

    media_file = MediaFileUpload(video_path, mimetype="video/*", resumable=True)

    history = load_upload_history()
    if video_path in history:
        print(f"⚠️ Video already uploaded: {video_path}")
        return

    for attempt in range(RETRIES):
        try:
            upload_request = youtube.videos().insert(
                part="snippet,status",
                body=request_body,
                media_body=media_file
            )
            response = upload_request.execute()
            video_id = response.get("id")

            print(f"✅ Uploaded: https://youtu.be/{video_id}")
            history[video_path] = video_id
            save_upload_history(history)

            send_log({
                "status": "upload_success",
                "video_id": video_id,
                "scheduled_time": upload_dt.isoformat(),
                "title": title,
                "file": video_path
            })

            return

        except HttpError as e:
            logging.error(f"Upload failed (attempt {attempt+1}): {e}")
            time.sleep(5)

    send_log({
        "status": "upload_failed",
        "file": video_path,
        "error": "Retries exhausted"
    })
    print("❌ Upload failed after retries.")

# Example usage:
# upload_video("output/final_video.mp4", "🔥 Best Deal Today!", "Check out this amazing deal...", ["deal", "discount", "amazon"])
