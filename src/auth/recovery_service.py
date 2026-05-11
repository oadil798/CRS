from __future__ import annotations
import secrets
from typing import Optional, Dict
from src.auth.password_utils import create_password_hash, hash_token
from src.database import users_repo, recovery_repo
from src.database.notifications_repo import add_notification

RECOVERY_TYPES = {
    "Forgot Password": "password",
    "Forgot Username": "username",
    "Forgot Both": "both",
}

def start_recovery(email: str, recovery_label: str) -> tuple[bool, str, Optional[str]]:
    user = users_repo.get_user_by_email(email)
    if not user:
        return False, "No account was found with that email address.", None
    token = secrets.token_urlsafe(32)
    recovery_type = RECOVERY_TYPES.get(recovery_label, "password")
    recovery_repo.create_token(user["id"], hash_token(token), recovery_type)
    add_notification(user["id"], "Account recovery requested", f"A {recovery_label.lower()} recovery token was generated.", "info")
    return True, "Recovery link generated. For FYP demo, the secure token is shown below instead of sending real email.", token

def inspect_token(token: str) -> Optional[Dict]:
    return recovery_repo.get_valid_token(hash_token(token.strip()))

def complete_recovery(token: str, new_username: Optional[str], new_password: Optional[str]) -> tuple[bool, str]:
    token_data = inspect_token(token)
    if not token_data:
        return False, "Recovery token is invalid, expired, or already used."
    recovery_type = token_data["recovery_type"]
    user_id = int(token_data["user_id"])
    try:
        if recovery_type in ["username", "both"]:
            if not new_username:
                return False, "Please enter a new username."
            users_repo.update_username(user_id, new_username)
        if recovery_type in ["password", "both"]:
            if not new_password or len(new_password) < 6:
                return False, "Please enter a new password with at least 6 characters."
            pw_hash, salt = create_password_hash(new_password)
            users_repo.update_password(user_id, pw_hash, salt)
        recovery_repo.mark_used(int(token_data["id"]))
        add_notification(user_id, "Account recovery completed", "Your account recovery changes were saved.", "success")
        return True, "Recovery completed successfully. You can now log in."
    except Exception as exc:
        return False, f"Recovery failed: {exc}"

def oauth_demo_message(provider: str) -> str:
    return f"{provider} login is shown as a demo/future enhancement. Local SQLite authentication is used for stable FYP demonstration."
