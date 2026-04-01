import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "healthcare.db"
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    with get_connection() as conn:
        conn.executescript(schema)


def seed_topics(rows: list[tuple[str, str, str]]) -> None:
    with get_connection() as conn:
        conn.executemany(
            "INSERT OR IGNORE INTO topics(name, info, disclaimer) VALUES (?, ?, ?)",
            rows,
        )
