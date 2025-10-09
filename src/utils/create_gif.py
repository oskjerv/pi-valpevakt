from PIL import Image
from pathlib import Path
import logging
from utils.timestamp_filename import timestamp_filename

def create_timelapse_gif(photo_dir="data/photos", output_dir="data/timelapses", max_photos=30):
    
    filename = timestamp_filename(prefix="gif", ext="gif")
    photo_dir = Path(photo_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    photos = sorted(photo_dir.glob("*.jpg"))
    if len(photos) < max_photos:
        logging.info(f"Not enough photos ({len(photos)}/{max_photos}) yet.")
        return None

    # Load and resize images for smaller file size
    frames = []
    for p in photos[:max_photos]:
        img = Image.open(p).convert("RGB")
        img = img.resize((640, 360))  # smaller resolution to reduce size
        frames.append(img)

    output_file = output_dir / filename
    frames[0].save(
        output_file,
        save_all=True,
        append_images=frames[1:],
        duration=500,   # ms per frame
        loop=0,
        optimize=True,
        quality=80,
    )

    # Remove source photos
    for p in photos[:max_photos]:
        p.unlink()

    logging.info(f"🎞️ Created timelapse: {output_file}")
    return output_file
