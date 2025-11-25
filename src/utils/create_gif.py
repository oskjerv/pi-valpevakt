import subprocess
from pathlib import Path
from PIL import Image, UnidentifiedImageError
import logging
from utils.timestamp_filename import timestamp_filename




def create_timelapse_mp4(photo_dir="data/photos", output_dir="data/timelapses", max_photos=30):
    photo_dir = Path(photo_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    created_videos = []
    photos = sorted(photo_dir.glob("*.jpg"))

    while len(photos) >= max_photos:
        temp_dir = photo_dir / "_tmp_mp4"
        temp_dir.mkdir(exist_ok=True)

        used_photos = []
        frame_id = 0

        # Prepare frames as sequential PNGs for ffmpeg
        for p in photos[:max_photos]:
            try:
                img = Image.open(p).convert("RGB")
                img = img.resize((640, 360))
                img.save(temp_dir / f"{frame_id:04d}.png")
                used_photos.append(p)
                frame_id += 1
            except (UnidentifiedImageError, OSError):
                logging.warning(f"Skipping corrupt image: {p}")
                p.unlink()

        if frame_id == 0:
            break

        output_file = output_dir / timestamp_filename(prefix="mp4", ext="mp4")

        # ffmpeg command to assemble frames into MP4 (H.264)
        subprocess.run([
            "ffmpeg", "-y",
            "-framerate", "2",
            "-i", str(temp_dir / "%04d.png"),
            "-pix_fmt", "yuv420p",
            "-vcodec", "libx264",
            "-crf", "23",
            str(output_file)
        ], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

        logging.info(f"🎞️ Created MP4 timelapse: {output_file}")
        created_videos.append(output_file)

        # Cleanup
        for f in temp_dir.glob("*.png"):
            f.unlink()
        temp_dir.rmdir()

        for p in used_photos:
            p.unlink()

        photos = sorted(photo_dir.glob("*.jpg"))

    return created_videos