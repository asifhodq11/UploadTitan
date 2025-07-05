import traceback
import json
import os
from topic_research import get_trending_topic
from script_generator import generate_script
from image_generator import generate_thumbnail
from voiceover_editor import create_short_video
from uploader import upload_video
from dashboard_logger import log_event

MAX_VIDEO_DURATION = 40  # seconds

def main():
    try:
        # 1. Pick a trending topic
        topic = get_trending_topic()
        log_event("topic", topic)

        # 2. Generate script
        script = generate_script(topic)
        log_event("script", script[:100] + "...")

        # 3. Create thumbnail image
        image_path = generate_thumbnail(script, topic)
        log_event("thumbnail", image_path)

        # 4. Create video with voiceover (<=40 sec)
        video_path, video_duration = create_short_video(script, image_path, topic)

        if video_duration > MAX_VIDEO_DURATION:
            log_event("error", f"Video too long: {video_duration} sec")
            print("Video exceeds 40 sec limit. Skipping upload.")
            return

        log_event("video_created", f"{video_path} ({video_duration}s)")

        # 5. Upload to YouTube
        upload_url = upload_video(video_path, topic)
        log_event("upload", upload_url)

    except Exception as e:
        error_msg = traceback.format_exc()
        log_event("fatal_error", error_msg)
        print("❌ Error occurred:", error_msg)

if __name__ == "__main__":
    main()
