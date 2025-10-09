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
    
    # --- 🌙 Brightness adjustments for low light ---
    # Optional: disable auto exposure if you want to manually control it
    # picam2.set_controls({"AeEnable": False})

    # Boost analogue gain (acts like ISO)
    # picam2.set_controls({"AnalogueGain": 6.0})  # Try values between 4.0 and 10.0

    # Extend exposure time (microseconds) — increases brightness but may blur motion
    # picam2.set_controls({"ExposureTime": 1000000})  # 100 ms

    # Optional: bump up exposure compensation (software tweak)
    # picam2.set_controls({"ExposureValue": 8.0})  # Range: -8.0 to +8.0

    
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
