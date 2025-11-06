import hashlib
import json
import os

_SECRET_SALT = "TryToCrackMeIfYouCanToGetPaidVersionForFree"  
_LICENSE_FILE = os.path.join("data", "user_license.json")

def _compute_hash(email: str) -> str:
    email = email.strip().lower()
    raw = (email + _SECRET_SALT).encode("utf-8")
    return hashlib.sha256(raw).hexdigest().upper()[:12]

def _expected_key(email: str) -> str:
    return f"FILEBUDDY-{_compute_hash(email)}"

def load_license() -> dict:
    """Return dict with 'email' and 'key' or empty dict."""
    if not os.path.exists(_LICENSE_FILE):
        return {}
    try:
        with open(_LICENSE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_license(email: str, key: str):
    os.makedirs(os.path.dirname(_LICENSE_FILE), exist_ok=True)
    with open(_LICENSE_FILE, "w", encoding="utf-8") as f:
        json.dump({"email": email.strip().lower(), "key": key.strip().upper()}, f, indent=2)

def is_valid_license(email: str, key: str) -> bool:
    """Stateless check for given email/key pair."""
    if not email or not key:
        return False
    return key.strip().upper() == _expected_key(email)

def activate_license(email: str, key: str) -> bool:
    """Validate and, if valid, save license to disk. Returns True on success."""
    if is_valid_license(email, key):
        save_license(email, key)
        return True
    return False

def is_pro_user() -> bool:
    """Read stored license and return True if valid."""
    data = load_license()
    if not data:
        return False
    return is_valid_license(data.get("email", ""), data.get("key", ""))
