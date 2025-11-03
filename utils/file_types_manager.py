import os, json

APP_FOLDER = os.path.join(os.getenv("APPDATA") or os.path.expanduser("~"), "FileBuddy")
DATA_FOLDER = os.path.join(APP_FOLDER, "data")
FILE_TYPES_PATH = os.path.join(DATA_FOLDER, "file_types.json")

DEFAULT_FILE_TYPES = {}

def ensure_data_folder():
    """Ensure the FileBuddy data folder exists, fall back if permission denied."""
    try:
        os.makedirs(DATA_FOLDER, exist_ok=True)
    except PermissionError:
        fallback = os.path.join(os.path.expanduser("~"), "FileBuddy")
        os.makedirs(fallback, exist_ok=True)
        return fallback
    return DATA_FOLDER

def load_file_types():
    """Load saved file type preferences, or create default if missing."""
    folder = ensure_data_folder()
    path = os.path.join(folder, "file_types.json")

    if not os.path.exists(path):
        save_file_types(DEFAULT_FILE_TYPES)
        return DEFAULT_FILE_TYPES

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return DEFAULT_FILE_TYPES

def save_file_types(filetypes: dict):
    """Save file type preferences safely."""
    folder = ensure_data_folder()
    path = os.path.join(folder, "file_types.json")

    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(filetypes, f, indent=4)
    except Exception as e:
        print(f"[FileBuddy] Failed to save file type preferences: {e}")
