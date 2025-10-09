import requests
import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import logging
from pathlib import Path
import os
import pickle




# --------------------------------------- #
# Function for collecting API-credentials #
# --------------------------------------- #

TOKEN_PATH = ".secrets/token.json"

def get_credentials():

    # Load credentials
    creds = Credentials.from_authorized_user_file(TOKEN_PATH)

    # Refresh if expired
    if not creds.valid:
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            # Save updated token
            with open(TOKEN_PATH, "w") as f:
                f.write(creds.to_json())
            print("🔄 Refreshed access token.")
        else:
            raise RuntimeError("❌ Credentials invalid and no refresh token available. Reauthorize the app.")
        
    return creds



# ----------------------------------------------------- #
# Function for uploading individual files to your album #
# ----------------------------------------------------- #

def upload_to_google_photos(image_path, album_id=None):
    creds = get_credentials()

    # 1️⃣ Upload the image bytes
    upload_url = "https://photoslibrary.googleapis.com/v1/uploads"
    headers = {
        "Authorization": f"Bearer {creds.token}",
        "Content-type": "application/octet-stream",
        "X-Goog-Upload-File-Name": image_path,
        "X-Goog-Upload-Protocol": "raw",
    }

    with open(image_path, "rb") as img:
        upload_token = requests.post(upload_url, data=img, headers=headers).text

    # 2️⃣ Create a media item (optionally in an album)
    create_url = "https://photoslibrary.googleapis.com/v1/mediaItems:batchCreate"
    payload = {
        "newMediaItems": [
            {
                "description": "Uploaded from Raspberry Pi",
                "simpleMediaItem": {"uploadToken": upload_token},
            }
        ]
    }
    if album_id:
        payload["albumId"] = album_id

    result = requests.post(create_url,
                           headers={"Authorization": f"Bearer {creds.token}",
                                    "Content-type": "application/json"},
                           data=json.dumps(payload))

    if result.status_code == 200:
        print("✅ Uploaded:", image_path)
        
    else:
        print("❌ Upload failed:", result.text)

# ------------------------------------------------------------------------------------- #        
# Function for uploading all files in folder with the help of upload_to_google_photos() #
# ------------------------------------------------------------------------------------- #

def upload_all_photos(config):
    # Load album ID
    #config = load_config()
    album_id = config["storage"]["albumid"]

    photos_dir = Path("data/timelapses")
    photos = sorted(photos_dir.glob("*.gif"))

    if not photos:
        logging.info("No photos to upload.")
        return

    logging.info(f"Found {len(photos)} photos to upload.")

    for photo in photos:
        try:
            logging.info(f"Uploading {photo} ...")
            uploaded = upload_to_google_photos(str(photo), album_id)
            photo.unlink()  # delete after successful upload
            logging.info(f"Uploaded and deleted: {photo.name}")
        except Exception as e:
            logging.error(f"Failed to upload {photo.name}: {e}")


if __name__ == '__main__':
    get_credentials()