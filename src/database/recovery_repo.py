from __future__ import annotations
from datetime import datetime, timedelta
from typing import Optional, Dict
from src.database.connection import get_connection

def create_token(user_id: int, token_hash: str, recovery_type: str, minutes_valid: int = 30) -> None:
    expires_at = (datetime.utcnow() + timedelta(minutes=minutes_valid)).isoformat(timespec="seconds")
    conn = get_connection()
    try:
        conn.execute("INSERT INTO recovery_tokens (user_id, token_hash, recovery_type, expires_at) VALUES (?, ?, ?, ?)", (user_id, token_hash, recovery_type, expires_at))
        conn.commit()
    finally:
        conn.close()

def get_valid_token(token_hash: str) -> Optional[Dict]:
    now = datetime.utcnow().isoformat(timespec="seconds")
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT rt.*, u.username, u.email, u.full_name FROM recovery_tokens rt JOIN users u ON u.id=rt.user_id WHERE rt.token_hash=? AND rt.used_at IS NULL AND rt.expires_at > ?",
            (token_hash, now),
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

def mark_used(token_id: int) -> None:
    conn = get_connection()
    try:
        conn.execute("UPDATE recovery_tokens SET used_at=CURRENT_TIMESTAMP WHERE id=?", (token_id,))
        conn.commit()
    finally:
        conn.close()
