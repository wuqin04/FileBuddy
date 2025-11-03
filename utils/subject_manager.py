import json, os

# Define app data folder inside APPDATA or fallback to user home
APP_FOLDER = os.path.join(os.getenv("APPDATA") or os.path.expanduser("~"), "FileBuddy")
DATA_FOLDER = os.path.join(APP_FOLDER, "data")
SUBJECTS_FILE = os.path.join(DATA_FOLDER, "subjects.json")

DEFAULT_SUBJECT = [
    {"name": "Mathematics", "include": True},
    {"name": "Programming", "include": True}
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
    """Load subjects list from JSON file, upgrading old format if necessary."""
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

        # --- Handle old format (list of strings) ---
        if all(isinstance(s, str) for s in subjects):
            subjects = [{"name": s, "include": True} for s in subjects]
            save_subjects(subjects)

        # --- Handle corrupted or empty data ---
        elif not isinstance(subjects, list) or len(subjects) == 0:
            raise ValueError("Subjects file is empty or invalid")

        return subjects

    except Exception:
        # File corrupted, unreadable, or invalid → reset to default
        save_subjects(DEFAULT_SUBJECT)
        return DEFAULT_SUBJECT

def save_subjects(subjects):
    folder = ensure_data_folder()
    path = os.path.join(folder, "subjects.json")

    # Normalize input
    if isinstance(subjects, dict) and "subjects" in subjects:
        raw = subjects["subjects"]
    else:
        raw = subjects

    normalized = []
    if isinstance(raw, list):
        for item in raw:
            if isinstance(item, str):
                # Old format: just a name string
                normalized.append({"name": item, "include": True})
            elif isinstance(item, dict):
                # Ensure required structure
                name = item.get("name") or item.get("subject") or item.get("title")
                if not name:
                    continue
                include = bool(item.get("include", True))
                normalized.append({"name": name, "include": include})
    else:
        normalized = []

    data = {"subjects": normalized}

    # --- Atomic write ---
    tmp_path = path + ".tmp"
    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        os.replace(tmp_path, path)  # safe atomic replacement
    finally:
        # Cleanup leftover temp if anything went wrong
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass
