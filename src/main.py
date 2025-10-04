import yaml
import logging
from pathlib import Path
from capture.photo_capture import capture_photo
from storage.uploader import upload_scp, upload_s3


logging.basicConfig(filename="logs/app.log", level=logging.INFO)

def main():
    with open("config/settings.yaml") as f:
        config = yaml.safe_load(f)

    photo_path = capture_photo(config)

    #if config["storage"]["method"] == "scp":
    #    upload_scp(str(photo_path), config["storage"]["remote"])
    #elif config["storage"]["method"] == "s3":
    #    upload_s3(str(photo_path), config["storage"]["aws"])
    #else:
    #    logging.warning("No valid upload method configured")

if __name__ == "__main__":
    main()
