from picamera2 import Picamera2, Preview
from pathlib import Path
import time
import logging

def capture_video(duration=10, resolution=(1920, 1080)):
    picam2 = Picamera2()
    config = picam2.create_video_configuration(main={"size": resolution})
    picam2.configure(config)

    picam2.start_recording("data/videos/temp.mp4")
    time.sleep(duration)
    picam2.stop_recording()

    output_dir = Path("data/videos")
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = output_dir / f"video_{int(time.time())}.mp4"

    Path("data/videos/temp.mp4").rename(filename)
    logging.info(f"Video saved: {filename}")
    return filename
