from __future__ import annotations
from typing import Optional, List, Dict
from src.database.connection import get_connection


def add_notification(user_id: Optional[int], title: str, message: str, notification_type: str = "info") -> int:
    conn = get_connection()
    try:
        cur = conn.execute(
            "INSERT INTO notifications (user_id, title, message, notification_type) VALUES (?, ?, ?, ?)",
            (user_id, title, message, notification_type),
        )
        conn.commit()
        return int(cur.lastrowid)
    finally:
        conn.close()


def add_broadcast_notification(title: str, message: str, notification_type: str = "info") -> int:
    """Create a separate notification row for every user so read/unread state stays private."""
    conn = get_connection()
    try:
        users = conn.execute("SELECT id FROM users").fetchall()
        for u in users:
            conn.execute(
                "INSERT INTO notifications (user_id, title, message, notification_type) VALUES (?, ?, ?, ?)",
                (u["id"], title, message, notification_type),
            )
        conn.commit()
        return len(users)
    finally:
        conn.close()


def get_notifications(user_id: int, limit: int = 100) -> List[Dict]:
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM notifications WHERE user_id=? OR user_id IS NULL ORDER BY created_at DESC LIMIT ?",
            (user_id, limit),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def mark_all_read(user_id: int) -> None:
    conn = get_connection()
    try:
        conn.execute("UPDATE notifications SET is_read=1 WHERE user_id=?", (user_id,))
        conn.commit()
    finally:
        conn.close()


def count_unread(user_id: int) -> int:
    conn = get_connection()
    try:
        return int(conn.execute("SELECT COUNT(*) FROM notifications WHERE user_id=? AND is_read=0", (user_id,)).fetchone()[0])
    finally:
        conn.close()
