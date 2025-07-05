# image_generator.py

from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import os

# Constants
WIDTH, HEIGHT = 720, 720
BACKGROUND_COLOR = (255, 255, 255)
TEXT_COLOR = (0, 0, 0)
FONT_PATH = "arial.ttf"  # Or "DejaVuSans-Bold.ttf" for Replit
ASSETS_FOLDER = "assets"
LOGO_FILENAME = "logo.png"

def generate_deal_image(title, price, discount, image_url, output_path="deal_card.jpg"):
    # Create base image
    image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(image)

    # Load fonts
    try:
        title_font = ImageFont.truetype(FONT_PATH, 36)
        price_font = ImageFont.truetype(FONT_PATH, 30)
        discount_font = ImageFont.truetype(FONT_PATH, 28)
    except:
        title_font = ImageFont.load_default()
        price_font = ImageFont.load_default()
        discount_font = ImageFont.load_default()

    # Load and paste product image
    try:
        response = requests.get(image_url, timeout=5)
        product_img = Image.open(BytesIO(response.content)).convert("RGB")
        product_img = product_img.resize((600, 400))
        image.paste(product_img, (60, 40))
    except Exception as e:
        print("Error loading product image:", e)

    # Draw title
    draw.text((40, 460), title[:80] + ("..." if len(title) > 80 else ""), fill=TEXT_COLOR, font=title_font)

    # Draw price and discount
    draw.text((40, 530), f"Price: {price}", fill=(0, 128, 0), font=price_font)
    draw.text((40, 580), f"Discount: {discount}", fill=(255, 0, 0), font=discount_font)

    # Optional: Add logo watermark (bottom right)
    logo_path = os.path.join(ASSETS_FOLDER, LOGO_FILENAME)
    if os.path.exists(logo_path):
        try:
            logo = Image.open(logo_path).convert("RGBA")
            logo.thumbnail((120, 120))
            image.paste(logo, (WIDTH - logo.width - 20, HEIGHT - logo.height - 20), logo)
        except Exception as e:
            print("Logo load error:", e)

    # Save final image
    image.save(output_path)
    return output_path
