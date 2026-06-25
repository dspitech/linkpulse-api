"""Couche de persistance SQLite pour les liens raccourcis.

Le chemin de la base est piloté par la variable d'environnement DB_PATH,
ce qui permet de pointer vers un volume Docker en staging/production tout
en gardant un fichier local simple en developpement.
"""

import os
import sqlite3
from contextlib import contextmanager
from datetime import UTC, datetime

DB_PATH = os.environ.get("DB_PATH", "linkpulse.db")


@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db() -> None:
    """Cree la table 'links' si elle n'existe pas encore."""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS links (
                code TEXT PRIMARY KEY,
                url TEXT NOT NULL,
                created_at TEXT NOT NULL,
                clicks INTEGER NOT NULL DEFAULT 0,
                active INTEGER NOT NULL DEFAULT 1
            )
            """
        )
        conn.commit()


def code_exists(code: str) -> bool:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT 1 FROM links WHERE code = ?",
            (code,),
        ).fetchone()

    return row is not None


def create_link(code: str, url: str) -> dict:
    created_at = datetime.now(UTC).isoformat()

    with get_connection() as conn:
        conn.execute(
            "INSERT INTO links (code, url, created_at, clicks, active) VALUES (?, ?, ?, 0, 1)",
            (code, url, created_at),
        )
        conn.commit()

    return {
        "code": code,
        "url": url,
        "created_at": created_at,
        "clicks": 0,
        "active": 1,
    }


def get_link(code: str) -> dict | None:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM links WHERE code = ?",
            (code,),
        ).fetchone()

    return dict(row) if row else None


def list_links(skip: int = 0, limit: int = 20) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM links ORDER BY created_at DESC LIMIT ? OFFSET ?",
            (limit, skip),
        ).fetchall()

    return [dict(row) for row in rows]


def increment_clicks(code: str) -> None:
    with get_connection() as conn:
        conn.execute(
            "UPDATE links SET clicks = clicks + 1 WHERE code = ?",
            (code,),
        )
        conn.commit()


def deactivate_link(code: str) -> bool:
    with get_connection() as conn:
        cursor = conn.execute(
            "UPDATE links SET active = 0 WHERE code = ?",
            (code,),
        )
        conn.commit()

    return cursor.rowcount > 0


def count_active_links() -> int:
    with get_connection() as conn:
        row = conn.execute("SELECT COUNT(*) AS total FROM links WHERE active = 1").fetchone()

    return row["total"] if row else 0
