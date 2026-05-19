from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

base = Path('frontend/public/assets/screenshots')
base.mkdir(parents=True, exist_ok=True)
texts = [
    ('login.png','Login Page'),
    ('upload.png','Upload Page'),
    ('results.png','Prediction Results'),
    ('history.png','History Page'),
    ('gradcam.png','Grad-CAM Visualization'),
    ('pdf.png','PDF Report Download')
]
for name, text in texts:
    img = Image.new('RGB',(900,600),(13,17,23))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype('arial.ttf', 42)
    except Exception:
        font = ImageFont.load_default()
    draw.rectangle([20,20,880,580], outline=(88,166,255), width=6)
    draw.text((60,100), text, fill=(255,255,255), font=font)
    draw.text((60,180), 'Skin Cancer Detection Demo', fill=(180,180,200), font=font)
    img.save(base / name)

frames = []
for text in ['Login', 'Upload', 'Results', 'History', 'Grad-CAM', 'PDF']:
    img = Image.new('RGB',(900,600),(13,17,23))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype('arial.ttf', 42)
    except Exception:
        font = ImageFont.load_default()
    draw.rectangle([20,20,880,580], outline=(88,166,255), width=6)
    draw.text((60,120), f'{text} Screen', fill=(255,255,255), font=font)
    draw.text((60,200), 'Skin Cancer Detection Demo', fill=(180,180,200), font=font)
    frames.append(img)

output = Path('docs/assets/demo.gif')
output.parent.mkdir(parents=True, exist_ok=True)
frames[0].save(output, save_all=True, append_images=frames[1:], duration=3000, loop=0)
