from __future__ import annotations
from typing import Optional, Dict, List
from src.database.connection import get_connection


def _dict(row) -> Optional[Dict]:
    return dict(row) if row else None


def create_user(full_name: str, username: str, email: str, password_hash: str, password_salt: str, role: str = "user", preferred_language: str = "English") -> int:
    conn = get_connection()
    try:
        cur = conn.execute(
            "INSERT INTO users (full_name, username, email, password_hash, password_salt, role, preferred_language) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (full_name.strip(), username.lower().strip(), email.lower().strip(), password_hash, password_salt, role, preferred_language),
        )
        conn.commit()
        return int(cur.lastrowid)
    finally:
        conn.close()


def get_user_by_identifier(identifier: str) -> Optional[Dict]:
    ident = identifier.lower().strip()
    conn = get_connection()
    try:
        return _dict(conn.execute("SELECT * FROM users WHERE lower(username)=? OR lower(email)=?", (ident, ident)).fetchone())
    finally:
        conn.close()


def get_user_by_email(email: str) -> Optional[Dict]:
    conn = get_connection()
    try:
        return _dict(conn.execute("SELECT * FROM users WHERE lower(email)=?", (email.lower().strip(),)).fetchone())
    finally:
        conn.close()


def get_user_by_id(user_id: int) -> Optional[Dict]:
    conn = get_connection()
    try:
        return _dict(conn.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone())
    finally:
        conn.close()


def list_users(limit: int = 200) -> List[Dict]:
    conn = get_connection()
    try:
        rows = conn.execute(
            """
            SELECT
                u.id,
                u.full_name,
                u.username,
                u.email,
                u.role,
                u.preferred_language,
                u.created_at,
                u.updated_at,
                COUNT(p.id) AS total_predictions
            FROM users u
            LEFT JOIN prediction_history p ON p.user_id = u.id
            GROUP BY u.id
            ORDER BY u.created_at DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def update_profile(user_id: int, full_name: str, username: str, email: str, preferred_language: str) -> None:
    conn = get_connection()
    try:
        conn.execute(
            "UPDATE users SET full_name=?, username=?, email=?, preferred_language=?, updated_at=CURRENT_TIMESTAMP WHERE id=?",
            (full_name.strip(), username.lower().strip(), email.lower().strip(), preferred_language, user_id),
        )
        conn.commit()
    finally:
        conn.close()


def admin_update_user(user_id: int, full_name: str, username: str, email: str, role: str, preferred_language: str) -> None:
    conn = get_connection()
    try:
        conn.execute(
            """
            UPDATE users
            SET full_name=?, username=?, email=?, role=?, preferred_language=?, updated_at=CURRENT_TIMESTAMP
            WHERE id=?
            """,
            (full_name.strip(), username.lower().strip(), email.lower().strip(), role, preferred_language, user_id),
        )
        conn.commit()
    finally:
        conn.close()


def update_username(user_id: int, username: str) -> None:
    conn = get_connection()
    try:
        conn.execute("UPDATE users SET username=?, updated_at=CURRENT_TIMESTAMP WHERE id=?", (username.lower().strip(), user_id))
        conn.commit()
    finally:
        conn.close()


def update_password(user_id: int, password_hash: str, password_salt: str) -> None:
    conn = get_connection()
    try:
        conn.execute("UPDATE users SET password_hash=?, password_salt=?, updated_at=CURRENT_TIMESTAMP WHERE id=?", (password_hash, password_salt, user_id))
        conn.commit()
    finally:
        conn.close()


def delete_user(user_id: int) -> None:
    conn = get_connection()
    try:
        conn.execute("DELETE FROM users WHERE id=?", (user_id,))
        conn.commit()
    finally:
        conn.close()


def count_users() -> int:
    conn = get_connection()
    try:
        return int(conn.execute("SELECT COUNT(*) FROM users").fetchone()[0])
    finally:
        conn.close()


def count_admins() -> int:
    conn = get_connection()
    try:
        return int(conn.execute("SELECT COUNT(*) FROM users WHERE role='admin'").fetchone()[0])
    finally:
        conn.close()
