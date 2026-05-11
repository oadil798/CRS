from pathlib import Path
import sys
import sqlite3
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.database.schema import initialise_database
from src.database.users_repo import create_user
from src.auth.password_utils import create_password_hash
from src.config import DEFAULT_ADMIN_USERNAME, DEFAULT_ADMIN_PASSWORD, DEFAULT_USER_USERNAME, DEFAULT_USER_PASSWORD
from src.database.notifications_repo import add_notification

def ensure_user(full_name, username, email, password, role):
    pw_hash, salt = create_password_hash(password)
    try:
        user_id = create_user(full_name, username, email, pw_hash, salt, role, "English")
        add_notification(user_id, "Welcome", f"{role.title()} demo account created successfully.", "success")
        print(f"Created {role}: {username}")
    except sqlite3.IntegrityError:
        print(f"Already exists: {username}")

if __name__ == "__main__":
    initialise_database()
    ensure_user("System Admin", DEFAULT_ADMIN_USERNAME, "admin@example.com", DEFAULT_ADMIN_PASSWORD, "admin")
    ensure_user("Demo User", DEFAULT_USER_USERNAME, "demo@example.com", DEFAULT_USER_PASSWORD, "user")
