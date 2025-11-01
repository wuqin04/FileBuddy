import json, os

SUBJECTS_FILE = os.path.join("data", "subjects.json")

def load_subjects():
    if not os.path.exists(SUBJECTS_FILE):
        os.makedirs(os.path.dirname(SUBJECTS_FILE), exist_ok=True)
        with open(SUBJECTS_FILE, "w") as f:
            json.dump({"subjects": []}, f, indent=4)
    with open(SUBJECTS_FILE, "r") as f:
        return json.load(f).get("subjects", [])

def save_subjects(subjects):
    os.makedirs(os.path.dirname(SUBJECTS_FILE), exist_ok=True)
    with open(SUBJECTS_FILE, "w") as f:
        json.dump({"subjects": subjects}, f, indent=4)
