from PIL import Image, ImageDraw, ImageFont
import random
import os
from topic_research import get_trending_topic
from job_logger import log_event

# Image constants
WIDTH, HEIGHT = 1080, 1920
FONTS = ["arial.ttf", "DejaVuSans-Bold.ttf"]  # Change or expand if needed
WATERMARK = "@QuickShortsBot"

# Color options for variety
BG_COLORS = ["#121212", "#1a1a1a", "#000000", "#202020"]
TEXT_COLORS = ["#FFDD00", "#FF4500", "#00FFFF", "#FFFFFF", "#1DB954"]

def get_font(size):
    for font_name in FONTS:
        try:
            return ImageFont.truetype(font_name, size)
        except IOError:
            continue
    return ImageFont.load_default()

def generate_image(topic=None, output_path="thumbnail.jpg"):
    if topic is None:
        topic = get_trending_topic()

    bg_color = random.choice(BG_COLORS)
    text_color = random.choice(TEXT_COLORS)

    image = Image.new("RGB", (WIDTH, HEIGHT), color=bg_color)
    draw = ImageDraw.Draw(image)

    title = f"{topic}".upper()

    # Auto font size fitting
    font_size = 100
    font = get_font(font_size)
    while font.getlength(title) > WIDTH - 100 and font_size > 10:
        font_size -= 5
        font = get_font(font_size)

    text_width, text_height = draw.textsize(title, font=font)
    text_x = (WIDTH - text_width) / 2
    text_y = HEIGHT / 2 - text_height / 2

    # Draw main text
    draw.text((text_x, text_y), title, font=font, fill=text_color)

    # Add watermark
    wm_font = get_font(30)
    draw.text((30, HEIGHT - 80), WATERMARK, font=wm_font, fill=(180, 180, 180))

    image.save(output_path)
    log_event("Image Generated", f"Saved {output_path} for topic: {topic}")
    return output_path
