import json
import os

# Define app data folder inside APPDATA or fallback to user home
APP_FOLDER = os.path.join(os.getenv("APPDATA") or os.path.expanduser("~"), "FileBuddy")
DATA_FOLDER = os.path.join(APP_FOLDER, "data")
SUBJECTS_FILE = os.path.join(DATA_FOLDER, "subjects.json")

def ensure_data_folder():
    """Ensure the data folder exists and is writable."""
    try:
        os.makedirs(DATA_FOLDER, exist_ok=True)
    except PermissionError:
        # Fallback to home directory if APPDATA is not accessible
        fallback = os.path.join(os.path.expanduser("~"), "FileBuddy", "data")
        os.makedirs(fallback, exist_ok=True)
        return fallback
    return DATA_FOLDER


def load_subjects():
    """Load subjects list from JSON file, creating a default if not found."""
    folder = ensure_data_folder()
    path = os.path.join(folder, "subjects.json")

    if not os.path.exists(path):
        save_subjects([])  # create default file
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f).get("subjects", [])
    except Exception:
        # corrupted or unreadable file, reset it
        save_subjects([])
        return []


def save_subjects(subjects):
    """Save the given subject list to JSON."""
    folder = ensure_data_folder()
    path = os.path.join(folder, "subjects.json")

    with open(path, "w", encoding="utf-8") as f:
        json.dump({"subjects": subjects}, f, indent=4)
