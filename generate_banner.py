import os
import requests
from PIL import Image, ImageDraw, ImageFont

# Define paths
BG_PATH = r"C:\Users\onkar\.gemini\antigravity-ide\brain\30b7f051-0530-48cd-836b-5680473b778c\ai_banner_background_1784972704396.png"
OUTPUT_PATH = r"c:\Users\onkar\Desktop\laptop Data 2025-26\khilarionkar05\banner.png"
FONTS_DIR = r"c:\Users\onkar\Desktop\laptop Data 2025-26\khilarionkar05\.fonts"

# Font URLs
ORBITRON_URL = "https://github.com/theleagueof/orbitron/raw/master/Orbitron%20Bold.ttf"
INTER_REGULAR_URL = "https://github.com/rsms/inter/raw/master/docs/font-files/Inter-Regular.ttf"
INTER_BOLD_URL = "https://github.com/rsms/inter/raw/master/docs/font-files/Inter-Bold.ttf"

def download_font(url, filename):
    os.makedirs(FONTS_DIR, exist_ok=True)
    filepath = os.path.join(FONTS_DIR, filename)
    if not os.path.exists(filepath):
        try:
            print(f"Downloading font from {url}...")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            with open(filepath, "wb") as f:
                f.write(response.content)
        except Exception as e:
            print(f"Failed to download font {filename}: {e}. Will use system fallback.")
    return filepath

def load_font(filepath, size, fallbacks):
    if os.path.exists(filepath):
        try:
            return ImageFont.truetype(filepath, size)
        except Exception as e:
            print(f"Failed to load downloaded font {filepath}: {e}")
    
    # Try system fallbacks
    for name in fallbacks:
        paths = [
            os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts", name),
            name
        ]
        for path in paths:
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()

def generate_banner():
    # 1. Download fonts (with try-except inside)
    orbitron_path = download_font(ORBITRON_URL, "Orbitron-Bold.ttf")
    inter_reg_path = download_font(INTER_REGULAR_URL, "Inter-Regular.ttf")
    inter_bold_path = download_font(INTER_BOLD_URL, "Inter-Bold.ttf")

    # 2. Open background image
    if not os.path.exists(BG_PATH):
        raise FileNotFoundError(f"Background image not found at: {BG_PATH}")
    
    img = Image.open(BG_PATH)
    print(f"Original background size: {img.size}")

    # Resize/Crop to exactly 1500 x 500
    target_width = 1500
    target_height = 500
    
    # Calculate aspect ratio resize
    img_ratio = img.width / img.height
    target_ratio = target_width / target_height

    if img_ratio > target_ratio:
        # Image is wider than target aspect ratio, resize by height
        new_height = target_height
        new_width = int(img_ratio * new_height)
    else:
        # Image is taller than target aspect ratio, resize by width
        new_width = target_width
        new_height = int(new_width / img_ratio)

    img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Crop center
    left = (new_width - target_width) / 2
    top = (new_height - target_height) / 2
    right = left + target_width
    bottom = top + target_height
    img_cropped = img_resized.crop((left, top, right, bottom))

    # Initialize drawing context
    draw = ImageDraw.Draw(img_cropped)

    # 3. Load Fonts with fallbacks
    font_name = load_font(orbitron_path, 64, ["trebucbd.ttf", "segoeuib.ttf", "arialbd.ttf"])
    font_title = load_font(inter_bold_path, 24, ["arialbd.ttf", "segoeuib.ttf", "trebucbd.ttf"])
    font_badge = load_font(inter_reg_path, 15, ["arial.ttf", "segoeui.ttf", "trebuc.ttf"])

    # Draw name "ONKAR KHILARI"
    # Accent colors
    color_primary = "#58A6FF"  # Blue
    color_secondary = "#00C896"  # Teal/Green
    color_accent = "#A855F7"  # Purple
    color_text = "#F0F6FC"  # Light Text
    color_muted = "#8B949E"  # Muted gray

    # Draw Name
    name_x, name_y = 100, 160
    draw.text((name_x, name_y), "ONKAR KHILARI", font=font_name, fill=color_text)

    # Draw Title: "AI ENGINEER" with letter spacing (we can simulate letter spacing by printing char-by-char)
    title_x, title_y = 105, 245
    title_text = "AI ENGINEER"
    # To draw letter spaced text:
    current_x = title_x
    for char in title_text:
        draw.text((current_x, title_y), char, font=font_title, fill=color_primary)
        # Advance current_x by character width + spacing
        char_w = draw.textlength(char, font=font_title)
        current_x += char_w + 10  # 10px tracking

    # Draw a thin horizontal accent line below the title
    line_y = 295
    draw.line((105, line_y, 450, line_y), fill=color_secondary, width=2)

    # 4. Draw Badges on the right
    # Badges array
    badges_col1 = ["Machine Learning", "Deep Learning", "Computer Vision", "Generative AI"]
    badges_col2 = ["Python", "FastAPI", "PyTorch", "TensorFlow"]

    badge_start_x1 = 800
    badge_start_x2 = 1100
    badge_start_y = 110
    row_height = 80

    # Draw Column 1 Badges
    for i, badge in enumerate(badges_col1):
        x = badge_start_x1
        y = badge_start_y + (i * row_height)
        
        # Calculate badge bounds based on text size
        text_w = draw.textlength(badge, font=font_badge)
        text_h = 18 # approximate height
        
        padding_x = 18
        padding_y = 10
        rect_left = x
        rect_top = y
        rect_right = x + text_w + (padding_x * 2)
        rect_bottom = y + text_h + (padding_y * 2)
        
        # Draw rounded rectangle background (semi-transparent dark)
        draw.rounded_rectangle(
            (rect_left, rect_top, rect_right, rect_bottom),
            radius=8,
            fill="#161B22",
            outline=color_accent,
            width=1
        )
        
        # Draw badge text
        draw.text((rect_left + padding_x, rect_top + padding_y), badge, font=font_badge, fill=color_text)

    # Draw Column 2 Badges
    for i, badge in enumerate(badges_col2):
        x = badge_start_x2
        y = badge_start_y + (i * row_height)
        
        # Calculate badge bounds based on text size
        text_w = draw.textlength(badge, font=font_badge)
        text_h = 18
        
        padding_x = 18
        padding_y = 10
        rect_left = x
        rect_top = y
        rect_right = x + text_w + (padding_x * 2)
        rect_bottom = y + text_h + (padding_y * 2)
        
        # Draw rounded rectangle background
        draw.rounded_rectangle(
            (rect_left, rect_top, rect_right, rect_bottom),
            radius=8,
            fill="#161B22",
            outline=color_secondary,
            width=1
        )
        
        # Draw badge text
        draw.text((rect_left + padding_x, rect_top + padding_y), badge, font=font_badge, fill=color_text)

    # Save output banner
    img_cropped.save(OUTPUT_PATH, "PNG")
    print(f"Successfully generated and saved banner to {OUTPUT_PATH}")

if __name__ == "__main__":
    generate_banner()
