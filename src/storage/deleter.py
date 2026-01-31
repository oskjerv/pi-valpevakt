#!/usr/bin/env python3
"""
Remove videos from the Google Photos album that are more than two days old.
Uses the same album and credentials as the uploader.
"""

import json
import logging
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

import requests
import yaml

# Ensure we run from project root so .secrets and config are found
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
os.chdir(PROJECT_ROOT)
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from storage.uploader import get_credentials

# --------------------------------------- #
# Configuration                           #
# --------------------------------------- #

TOKEN_PATH = ".secrets/token.json"
CONFIG_PATH = PROJECT_ROOT / "config" / "storage_settings.yaml"
BASE_URL = "https://photoslibrary.googleapis.com/v1"
MAX_AGE_DAYS = 2
BATCH_SIZE = 50  # API limit for batchRemoveMediaItems

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def load_config():
    """Load storage config (album ID)."""
    if not CONFIG_PATH.exists():
        logging.error("Config not found: %s", CONFIG_PATH)
        sys.exit(1)
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)


def list_media_in_album(creds, album_id: str):
    """List all media items in the album (with pagination)."""
    url = f"{BASE_URL}/mediaItems:search"
    headers = {
        "Authorization": f"Bearer {creds.token}",
        "Content-Type": "application/json",
    }
    all_items = []
    page_token = None

    while True:
        body = {"albumId": album_id, "pageSize": 100}
        if page_token:
            body["pageToken"] = page_token

        resp = requests.post(url, headers=headers, json=body)
        if resp.status_code != 200:
            logging.error("Search failed: %s %s", resp.status_code, resp.text)
            return []

        data = resp.json()
        items = data.get("mediaItems") or []
        all_items.extend(items)
        page_token = data.get("nextPageToken")
        if not page_token:
            break

    return all_items


def filter_videos_older_than(items, days: int):
    """Return items that are videos and older than `days` days."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    result = []
    for item in items:
        mime = (item.get("mimeType") or "").lower()
        if "video" not in mime:
            continue
        meta = item.get("mediaMetadata") or {}
        creation = meta.get("creationTime")
        if not creation:
            continue
        try:
            # RFC3339 e.g. "2024-12-01T10:00:00Z"
            created = datetime.fromisoformat(creation.replace("Z", "+00:00"))
            if created < cutoff:
                result.append(item)
        except (ValueError, TypeError):
            continue
    return result


def remove_from_album(creds, album_id: str, media_item_ids: list):
    """Remove media items from the album (up to 50 per call)."""
    if not media_item_ids:
        return True
    url = f"{BASE_URL}/albums/{album_id}:batchRemoveMediaItems"
    headers = {
        "Authorization": f"Bearer {creds.token}",
        "Content-Type": "application/json",
    }
    body = {"mediaItemIds": media_item_ids}
    resp = requests.post(url, headers=headers, json=body)
    if resp.status_code != 200:
        logging.error("batchRemoveMediaItems failed: %s %s", resp.status_code, resp.text)
        return False
    return True


def remove_old_videos(storage_config):
    """
    Remove videos from the Google Photos album that are older than MAX_AGE_DAYS.
    Can be called from main.py with the same storage_config used for uploads.

    Args:
        storage_config: Config dict with storage.albumid (e.g. from storage_settings.yaml)
    """
    album_id = (storage_config or {}).get("storage", {}).get("albumid")
    if not album_id or album_id == "albumid":
        logging.error("Invalid or missing storage.albumid; skipping old video removal.")
        return

    try:
        creds = get_credentials()
    except Exception as e:
        logging.error("Deleter: failed to get credentials: %s", e)
        return

    logging.info("Listing media in album %s ...", album_id[:20] + "...")
    items = list_media_in_album(creds, album_id)
    logging.info("Found %d item(s) in album.", len(items))

    to_remove = filter_videos_older_than(items, MAX_AGE_DAYS)
    if not to_remove:
        logging.info("No videos older than %d days to remove.", MAX_AGE_DAYS)
        return

    ids = [item["id"] for item in to_remove]
    logging.info("Removing %d video(s) older than %d days.", len(ids), MAX_AGE_DAYS)

    for i in range(0, len(ids), BATCH_SIZE):
        batch = ids[i : i + BATCH_SIZE]
        if not remove_from_album(creds, album_id, batch):
            logging.error("Deleter: failed to remove a batch; stopping.")
            return

    logging.info("Done. Removed %d video(s).", len(ids))


def main():
    config = load_config()
    album_id = config.get("storage", {}).get("albumid")
    if not album_id or album_id == "albumid":
        logging.error("Invalid or missing storage.albumid in %s", CONFIG_PATH)
        sys.exit(1)

    remove_old_videos(config)
    # If we were run as script, we don't sys.exit on deleter failure (already logged)


if __name__ == "__main__":
    main()
