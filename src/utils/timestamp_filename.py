from datetime import datetime


def timestamp_filename(prefix="image", ext="jpg"):
    """
    Generates a filename with current datetime.
    Format: prefix_yyyymmdd_hhmmss.ext
    Example: image_20251004_203115.jpg
    """
    now = datetime.now()
    return f"{prefix}_{now.strftime('%Y%m%d_%H%M%S')}.{ext}"