import sqlite3
from pathlib import Path

DB_PATH = Path("data/settings.db")


def _conn():
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)")
    conn.commit()
    return conn


def get(key, default=None):
    with _conn() as conn:
        row = conn.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
        return row[0] if row else default


def set(key, value):
    with _conn() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
            (key, str(value)),
        )
        conn.commit()
