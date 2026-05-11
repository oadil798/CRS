from __future__ import annotations
import json
from typing import Dict, List
import pandas as pd
from src.database.connection import get_connection


def add_prediction(user_id: int, mode: str, values: Dict[str, float], result: Dict) -> int:
    conn = get_connection()
    try:
        cur = conn.execute(
            '''INSERT INTO prediction_history
            (user_id, mode, N, P, K, temperature, humidity, ph, rainfall, recommended_crop, confidence, confidence_level, top_candidates_json, warnings_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (
                user_id,
                mode,
                values["N"],
                values["P"],
                values["K"],
                values["temperature"],
                values["humidity"],
                values["ph"],
                values["rainfall"],
                result["recommended_crop"],
                result["confidence"],
                result["confidence_level"],
                json.dumps(result["top_candidates"]),
                json.dumps(result.get("warnings", [])),
            ),
        )
        conn.commit()
        return int(cur.lastrowid)
    finally:
        conn.close()


def get_user_predictions(user_id: int, limit: int = 200) -> List[Dict]:
    conn = get_connection()
    try:
        rows = conn.execute(
            """
            SELECT *
            FROM prediction_history
            WHERE user_id=?
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (user_id, limit),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_all_predictions(limit: int = 1000) -> List[Dict]:
    conn = get_connection()
    try:
        rows = conn.execute(
            """
            SELECT
                p.*,
                u.full_name,
                u.username,
                u.email
            FROM prediction_history p
            JOIN users u ON u.id=p.user_id
            ORDER BY p.created_at DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def delete_prediction(prediction_id: int) -> None:
    conn = get_connection()
    try:
        conn.execute("DELETE FROM prediction_history WHERE id=?", (prediction_id,))
        conn.commit()
    finally:
        conn.close()


def delete_user_predictions(user_id: int) -> None:
    conn = get_connection()
    try:
        conn.execute("DELETE FROM prediction_history WHERE user_id=?", (user_id,))
        conn.commit()
    finally:
        conn.close()


def get_stats() -> Dict:
    conn = get_connection()
    try:
        total = int(conn.execute("SELECT COUNT(*) FROM prediction_history").fetchone()[0])
        avg = conn.execute("SELECT AVG(confidence) FROM prediction_history").fetchone()[0] or 0
        modes = [dict(r) for r in conn.execute("SELECT mode, COUNT(*) as count FROM prediction_history GROUP BY mode").fetchall()]
        crops = [dict(r) for r in conn.execute("SELECT recommended_crop, COUNT(*) as count FROM prediction_history GROUP BY recommended_crop ORDER BY count DESC LIMIT 10").fetchall()]
        active_users = int(conn.execute("SELECT COUNT(DISTINCT user_id) FROM prediction_history").fetchone()[0])
        return {"total": total, "average_confidence": float(avg), "mode_usage": modes, "top_crops": crops, "active_users": active_users}
    finally:
        conn.close()


def to_dataframe(rows: List[Dict]) -> pd.DataFrame:
    if not rows:
        return pd.DataFrame()
    df = pd.DataFrame(rows)
    if "confidence" in df:
        df["confidence_percent"] = (df["confidence"].astype(float) * 100).round(2)
    return df
