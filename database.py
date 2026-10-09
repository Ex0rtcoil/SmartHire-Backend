import sqlite3
import json
from pathlib import Path
from datetime import datetime, timezone

DB_PATH = Path(__file__).resolve().parent / "smarthire.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS resume_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                skills TEXT NOT NULL,
                education TEXT NOT NULL,
                experience_years REAL,
                candidate_summary TEXT,
                recommended_roles TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)


def save_result(filename, result):
    with get_connection() as conn:
        cursor = conn.execute("""
            INSERT INTO resume_results (
                filename,
                skills,
                education,
                experience_years,
                candidate_summary,
                recommended_roles,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            filename,
            json.dumps(result.get("skills", [])),
            json.dumps(result.get("education", [])),
            result.get("experience_years", 0),
            result.get("candidate_summary", ""),
            json.dumps(result.get("recommended_roles", [])),
            datetime.now(timezone.utc).isoformat()
        ))

        return cursor.lastrowid