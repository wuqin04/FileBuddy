import os
import sys
import json

APP_FOLDER = os.path.join(os.getenv("APPDATA") or os.path.expanduser("~"), "FileBuddy")
CONFIG_PATH = os.path.join(APP_FOLDER, "configs.json")

DEFAULT_CONFIG = {
    "theme": "light",
    "last_download_path": "",
    "last_output_path": ""
}

def ensure_appdata_folder():
    try:
        os.makedirs(APP_FOLDER, exist_ok=True)
    except PermissionError:
        # fallback: use user home if APPDATA is blocked
        fallback = os.path.join(os.path.expanduser("~"), "FileBuddy")
        os.makedirs(fallback, exist_ok=True)
        return fallback
    return APP_FOLDER

def load_config():
    folder = ensure_appdata_folder()
    path = os.path.join(folder, "configs.json")

    if not os.path.exists(path):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(config):
    folder = ensure_appdata_folder()
    path = os.path.join(folder, "configs.json")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)
