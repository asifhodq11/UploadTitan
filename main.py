import os
import logging
from threading import Thread

from image_generator import generate_images_from_prompt
from audio_generator import generate_audio
from video_creator import create_video_from_images
from youtube_uploader import upload_video
from title_description_generator import generate_title_description

# Optional: You can control prompts based on trending topics
from trending_scraper import get_trending_prompts

# Import Flask dashboard app
from dashboard.app import app as flask_app

logging.basicConfig(level=logging.INFO)

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def run_pipeline():
    base_output_dir = "output"
    ensure_dir(base_output_dir)

    prompts = get_trending_prompts(limit=1)  # You can change this for more videos
    for idx, prompt in enumerate(prompts):
        video_id = f"video_{idx}"
        video_dir = os.path.join(base_output_dir, video_id)
        img_dir = os.path.join(video_dir, "images")
        audio_path = os.path.join(video_dir, "audio.mp3")
        final_video_path = os.path.join(video_dir, "final_video.mp4")

        ensure_dir(img_dir)

        try:
            logging.info(f"🎯 Starting pipeline for: {prompt}")

            # Step 1: Generate Images
            generate_images_from_prompt(prompt, output_dir=img_dir)

            # Step 2: Generate Audio
            generate_audio(prompt, output_path=audio_path)

            # Step 3: Create Video
            create_video_from_images(img_dir, audio_path, final_video_path)

            # Step 4: Generate YouTube Title & Description
            title, description, tags = generate_title_description(prompt)

            # Step 5: Upload to YouTube
            upload_video(final_video_path, title, description, tags)

            logging.info(f"✅ Done: {video_id}")

        except Exception as e:
            logging.error(f"❌ Pipeline failed for {video_id}: {e}")

def run_dashboard():
    flask_app.run(host="0.0.0.0", port=3000)

if __name__ == "__main__":
    # Start the dashboard in a separate thread
    Thread(target=run_dashboard).start()

    # Run the video generation/upload pipeline
    run_pipeline()
