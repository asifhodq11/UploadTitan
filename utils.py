import os
import logging
from moviepy.editor import VideoFileClip, AudioFileClip

def setup_logger(name="UploadTitan", level=logging.INFO):
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        logger.addHandler(handler)
    return logger

def trim_video(input_path, output_path, max_duration=40):
    clip = VideoFileClip(input_path)
    clip = clip.subclip(0, min(max_duration, clip.duration))
    clip.write_videofile(output_path, codec='libx264', audio_codec='aac')
    clip.close()

def trim_audio(input_path, output_path, max_duration=40):
    clip = AudioFileClip(input_path)
    clip = clip.subclip(0, min(max_duration, clip.duration))
    clip.write_audiofile(output_path)
    clip.close()

def get_duration(filepath):
    if filepath.endswith('.mp4'):
        return VideoFileClip(filepath).duration
    elif filepath.endswith('.mp3'):
        return AudioFileClip(filepath).duration
    return 0

def clean_temp(folder="temp"):
    if not os.path.exists(folder):
        return
    for file in os.listdir(folder):
        try:
            os.remove(os.path.join(folder, file))
        except Exception as e:
            print(f"Failed to delete {file}: {e}")

def file_size(path):
    return round(os.path.getsize(path) / 1024 / 1024, 2)  # in MB
