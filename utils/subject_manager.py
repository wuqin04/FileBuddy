import json
import os

# Define app data folder inside APPDATA or fallback to user home
APP_FOLDER = os.path.join(os.getenv("APPDATA") or os.path.expanduser("~"), "FileBuddy")
DATA_FOLDER = os.path.join(APP_FOLDER, "data")
SUBJECTS_FILE = os.path.join(DATA_FOLDER, "subjects.json")

DEFAULT_SUBJECT = [
    "Mathematics",
    "Physics",
    "English",
    "Chemistry",
    "Biology"
]

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
    """Load subjects list from JSON file, creating or repairing defaults if needed."""
    folder = ensure_data_folder()
    path = os.path.join(folder, "subjects.json")

    # If file missing → create defaults
    if not os.path.exists(path):
        save_subjects(DEFAULT_SUBJECT)
        return DEFAULT_SUBJECT

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            subjects = data.get("subjects", [])

            # Handle corrupted or empty data
            if not isinstance(subjects, list) or len(subjects) == 0:
                raise ValueError("Subjects file is empty or invalid")

            return subjects

    except Exception:
        # File corrupted, unreadable, or invalid → reset to default
        save_subjects(DEFAULT_SUBJECT)
        return DEFAULT_SUBJECT



def save_subjects(subjects):
    """Save the given subject list to JSON."""
    folder = ensure_data_folder()
    path = os.path.join(folder, "subjects.json")

    with open(path, "w", encoding="utf-8") as f:
        json.dump({"subjects": subjects}, f, indent=4)
