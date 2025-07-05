import os
import subprocess
import uuid
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
from utils import upload_to_telegram, add_watermark

MAX_DURATION = 40  # seconds

def create_video(image_folder, audio_path, output_folder="videos", watermark_path=None):
    os.makedirs(output_folder, exist_ok=True)
    
    image_files = sorted([
        os.path.join(image_folder, f)
        for f in os.listdir(image_folder)
        if f.lower().endswith(('.png', '.jpg', '.jpeg'))
    ])
    
    if not image_files:
        raise Exception("No images found to create video.")
    
    audio = AudioFileClip(audio_path)
    audio_duration = min(audio.duration, MAX_DURATION)
    
    # Dynamic duration per image
    image_duration = audio_duration / len(image_files)

    clips = []
    for img_path in image_files:
        clip = ImageClip(img_path).set_duration(image_duration)
        clips.append(clip)
    
    final_clip = concatenate_videoclips(clips, method="compose").set_audio(audio).subclip(0, MAX_DURATION)
    
    filename = f"{uuid.uuid4().hex[:8]}.mp4"
    raw_video_path = os.path.join(output_folder, filename)
    final_clip.write_videofile(raw_video_path, fps=24, codec="libx264", audio_codec="aac")

    # Add watermark if provided
    final_video_path = raw_video_path
    if watermark_path:
        watermarked_path = os.path.join(output_folder, f"wm_{filename}")
        add_watermark(raw_video_path, watermark_path, watermarked_path)
        final_video_path = watermarked_path

    return final_video_path

def add_watermark(input_path, watermark_path, output_path):
    command = [
        "ffmpeg", "-y", "-i", input_path, "-i", watermark_path,
        "-filter_complex", "overlay=W-w-10:H-h-10",
        "-codec:a", "copy", output_path
    ]
    subprocess.run(command, check=True)

def process_video_pipeline(image_folder, audio_path, watermark_path, telegram_token, telegram_chat_id):
    try:
        final_video_path = create_video(image_folder, audio_path, watermark_path=watermark_path)
        upload_to_telegram(final_video_path, telegram_token, telegram_chat_id)
        print("✅ Video created and uploaded successfully.")
    except Exception as e:
        print(f"❌ Failed to create video: {e}")
