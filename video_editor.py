import os
import time
import logging
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
import requests

# Configuration
MAX_DURATION = 40  # in seconds
MAX_RETRIES = 3
FPS = 24
VIDEO_RESOLUTION_HEIGHT = 1280  # pixels
DASHBOARD_ENDPOINT = "https://your-dashboard.vercel.app/api/log"  # Optional: your logging backend

def send_log(data):
    try:
        requests.post(DASHBOARD_ENDPOINT, json=data, timeout=5)
    except Exception as e:
        logging.warning(f"Failed to send dashboard log: {e}")

def create_video_from_images(images_dir, audio_path, output_path, retry_count=0):
    try:
        logging.info(f"Starting video creation attempt {retry_count + 1}")
        start_time = time.time()

        # Collect image files
        image_files = sorted([
            os.path.join(images_dir, file)
            for file in os.listdir(images_dir)
            if file.lower().endswith((".png", ".jpg", ".jpeg"))
        ])
        if not image_files:
            raise FileNotFoundError(f"No images found in {images_dir}")

        # Load audio
        audio = AudioFileClip(audio_path)
        audio_duration = audio.duration

        # Set duration per image
        per_image_duration = min(MAX_DURATION / len(image_files), 5)  # Max 5s/image
        clips = [
            ImageClip(img)
            .set_duration(per_image_duration)
            .resize(height=VIDEO_RESOLUTION_HEIGHT)
            .set_position("center")
            for img in image_files
        ]

        # Merge clips and audio
        final_video = concatenate_videoclips(clips).set_audio(audio)
        final_duration = final_video.duration

        if final_duration > MAX_DURATION:
            raise ValueError(f"Generated video is {final_duration:.2f}s, exceeds 40s limit")

        final_video.write_videofile(output_path, fps=FPS)
        elapsed = round(time.time() - start_time, 2)

        send_log({
            "status": "success",
            "duration": final_duration,
            "retry": retry_count,
            "time_taken": elapsed,
            "video_path": output_path
        })

        print(f"✅ Video created: {output_path} ({final_duration:.2f}s, attempt {retry_count + 1})")

    except Exception as e:
        logging.error(f"[Attempt {retry_count + 1}] Error: {e}")

        if retry_count < MAX_RETRIES:
            print(f"⚠️ Retrying... ({retry_count + 1}/{MAX_RETRIES})")
            create_video_from_images(images_dir, audio_path, output_path, retry_count + 1)
        else:
            failed_path = output_path.replace(".mp4", "_failed.mp4")
            send_log({
                "status": "failed",
                "error": str(e),
                "retry": retry_count,
                "video_path": failed_path
            })
            print(f"❌ All retries failed. Logged failure for: {failed_path}")
