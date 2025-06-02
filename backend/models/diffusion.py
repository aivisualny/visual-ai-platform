import os
import uuid
from PIL import Image, ImageDraw

def generate_diffusion_image():
    width, height = 64, 64
    image = Image.new('L', (width, height), color=255)
    draw = ImageDraw.Draw(image)
    draw.rectangle([10, 10, 54, 54], outline=0, width=3)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.join(base_dir, "..", "static", "generated_images")
    os.makedirs(static_dir, exist_ok=True)

    filename = f"{uuid.uuid4().hex}_diff.png"
    save_path = os.path.join(static_dir, filename)
    image.save(save_path)

    return f"/static/generated_images/{filename}"
