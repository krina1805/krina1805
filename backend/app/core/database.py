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
    statements = [statement.strip() for statement in schema.split(";") if statement.strip()]

    with get_connection() as conn:
        for statement in statements:
            try:
                conn.execute(statement)
            except sqlite3.OperationalError as exc:
                if "already exists" not in str(exc).lower():
                    raise


def seed_topics(rows: list[tuple[str, str, str]]) -> None:
    with get_connection() as conn:
        conn.executemany(
            "INSERT OR IGNORE INTO topics(name, info, disclaimer) VALUES (?, ?, ?)",
            rows,
        )
