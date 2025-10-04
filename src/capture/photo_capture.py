from picamera2 import Picamera2, Preview
import time
from pathlib import Path
import logging
import yaml

from utils.timestamp_filename import timestamp_filename

def capture_photo(config):
    picam2 = Picamera2()
    res = tuple(config["camera"]["resolution"])
    warmup = config["camera"]["warmup_time"]

    camera_config = picam2.create_still_configuration(main={"size": res})
    picam2.configure(camera_config)

    if config["camera"]["preview"]:
        picam2.start_preview(Preview.NULL)
    picam2.start()

    time.sleep(warmup)
    output_dir = Path("data/photos")
    output_dir.mkdir(parents=True, exist_ok=True)

    filename = output_dir / timestamp_filename("photo", "jpg")
    
    #filename = output_dir / f"photo_{int(time.time())}.jpg"
    
    #print(filename)
    #print(filename2)
    picam2.capture_file(str(filename))
    picam2.stop()

    logging.info(f"Photo saved: {filename}")
    return filename
