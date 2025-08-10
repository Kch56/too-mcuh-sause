from pathlib import Path
from PIL import Image, ImageOps
import pillow_heif

# Register HEIC/HEIF opener
pillow_heif.register_heif_opener()

# Source and destination
SRC_FOLDER = Path("static/images/Food pics")  # where your current images are
DST_FOLDER = Path("static/images/food")       # new clean folder for JPEGs

# Create destination folder if it doesn't exist
DST_FOLDER.mkdir(parents=True, exist_ok=True)

# File types we will handle
ALLOWED_EXTS = {".heic", ".heif", ".jpg", ".jpeg", ".png", ".webp"}

count = 0
for img_path in SRC_FOLDER.iterdir():
    if img_path.suffix.lower() not in ALLOWED_EXTS:
        continue

    try:
        # Open and auto-rotate based on EXIF
        with Image.open(img_path) as img:
            img = ImageOps.exif_transpose(img)

            # Optional resize if image is too big
            MAX_SIZE = 2400
            if max(img.size) > MAX_SIZE:
                img.thumbnail((MAX_SIZE, MAX_SIZE))

            # Convert to RGB and save as JPEG
            out_path = DST_FOLDER / f"{img_path.stem}.jpg"
            img.convert("RGB").save(out_path, "JPEG", quality=88, optimize=True, progressive=True)

            print(f"✅ Converted: {img_path.name} -> {out_path.name}")
            count += 1
    except Exception as e:
        print(f"❌ Failed to convert {img_path.name}: {e}")

print(f"\n🎯 Done! Converted {count} images to JPEG in {DST_FOLDER}")
