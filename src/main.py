import yaml
import logging
from pathlib import Path
from capture.photo_capture import capture_photo
from storage.uploader import upload_to_google_photos, upload_all_photos
from utils.create_gif import create_timelapse_mp4



logging.basicConfig(filename="logs/app.log", level=logging.INFO)

def main():
    with open("config/cam_settings.yaml") as f:
        config = yaml.safe_load(f)
    with open("config/storage_settings.yaml") as f:
        storage_config = yaml.safe_load(f)

    # Take the photo
    capture_photo(config)
    # Creates a .gif if there are 30 images, and deletes after
    create_timelapse_mp4(max_photos = 30)
    # Uploads the gifs (if there are any), and deletes afer.
    upload_all_photos(storage_config)

if __name__ == "__main__":
    main()
