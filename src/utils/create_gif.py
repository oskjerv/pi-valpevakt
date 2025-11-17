from PIL import Image
from pathlib import Path
import logging
from utils.timestamp_filename import timestamp_filename

def create_timelapse_gif(photo_dir="data/photos", output_dir="data/timelapses", max_photos=30):
    photo_dir = Path(photo_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    created_gifs = []
    photos = sorted(photo_dir.glob("*.jpg"))

    while len(photos) >= max_photos:
        frames = []
        used_photos = []

        for p in photos[:max_photos]:
            try:
                img = Image.open(p).convert("RGB")
                img = img.resize((640, 360))
                frames.append(img)
                used_photos.append(p)
            except (UnidentifiedImageError, OSError) as e:
                logging.warning(f"Skipping corrupt image {p.name}: {e}")
                p.unlink()  # Remove the problematic file

        if len(frames) == 0:
            logging.warning("No valid images found in this batch.")
            break

        filename = timestamp_filename(prefix="gif", ext="gif")
        output_file = output_dir / filename
        frames[0].save(
            output_file,
            save_all=True,
            append_images=frames[1:],
            duration=500,
            loop=0,
            optimize=True,
            quality=80,
        )
        logging.info(f"🎞️ Created timelapse: {output_file}")
        created_gifs.append(str(output_file))

        # Only remove successfully used photos
        for p in used_photos:
            p.unlink()

        photos = sorted(photo_dir.glob("*.jpg"))

    if len(created_gifs) == 0:
        logging.info(f"Not enough valid photos to create a GIF.")
    return created_gifs