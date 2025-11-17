from PIL import Image
from pathlib import Path
import logging
from utils.timestamp_filename import timestamp_filename

def create_timelapse_gif(photo_dir="data/photos", output_dir="data/timelapses", max_photos=30):
    photo_dir = Path(photo_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    photos = sorted(photo_dir.glob("*.jpg"))
    if len(photos) < max_photos:
        logging.info(f"Not enough photos ({len(photos)}/{max_photos}) yet.")
        return None

    gif_files = []
    # Process in batches of max_photos
    while len(photos) >= max_photos:
        # Generate a unique filename for this batch GIF
        filename = timestamp_filename(prefix="gif", ext="gif")
        frames = []
        # Collect up to 30 images for this batch
        for p in photos[:max_photos]:
            img = Image.open(p).convert("RGB")
            img = img.resize((640, 360))
            frames.append(img)
        output_file = output_dir / filename

        # Save as animated GIF (first frame + append rest)
        frames[0].save(
            output_file,
            save_all=True,
            append_images=frames[1:],
            duration=500,
            loop=0,
            optimize=True,
            quality=80
        )

        # Remove the 30 source photos we just used
        for p in photos[:max_photos]:
            p.unlink()

        logging.info(f"🎞️ Created timelapse: {output_file}")
        gif_files.append(output_file)

        # Refresh the list of remaining images
        photos = sorted(photo_dir.glob("*.jpg"))

    return gif_files
