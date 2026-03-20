"""SQLite metadata store for the show catalog."""

import json
import sqlite3
from contextlib import contextmanager

from backend.core.config import settings
from backend.models.schemas import ScriptFeatures, ShowInfo


def _db_path() -> str:
    url = settings.database_url
    if url.startswith("sqlite:///"):
        return url[len("sqlite:///"):]
    return url


@contextmanager
def _get_conn():
    conn = sqlite3.connect(_db_path())
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    """Create tables if they don't exist."""
    with _get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS shows (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                year INTEGER,
                network TEXT DEFAULT '',
                imdb_id TEXT DEFAULT '',
                num_episodes_analyzed INTEGER DEFAULT 0,
                features_json TEXT DEFAULT '{}',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


def upsert_show(show: ShowInfo) -> None:
    """Insert or update a show in the catalog."""
    features_json = show.features.model_dump_json() if show.features else "{}"
    with _get_conn() as conn:
        conn.execute(
            """
            INSERT INTO shows (id, title, year, network, num_episodes_analyzed, features_json, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(id) DO UPDATE SET
                title = excluded.title,
                year = excluded.year,
                network = excluded.network,
                num_episodes_analyzed = excluded.num_episodes_analyzed,
                features_json = excluded.features_json,
                updated_at = CURRENT_TIMESTAMP
            """,
            (show.id, show.title, show.year, show.network, show.num_episodes_analyzed, features_json),
        )


def get_show(show_id: str) -> ShowInfo | None:
    """Get a show by ID."""
    with _get_conn() as conn:
        row = conn.execute("SELECT * FROM shows WHERE id = ?", (show_id,)).fetchone()
        if not row:
            return None
        return _row_to_show(row)


def list_shows() -> list[ShowInfo]:
    """List all shows in the catalog."""
    with _get_conn() as conn:
        rows = conn.execute("SELECT * FROM shows ORDER BY title").fetchall()
        return [_row_to_show(r) for r in rows]


def search_shows(query: str) -> list[ShowInfo]:
    """Search shows by title (case-insensitive substring match)."""
    with _get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM shows WHERE LOWER(title) LIKE ? ORDER BY title",
            (f"%{query.lower()}%",),
        ).fetchall()
        return [_row_to_show(r) for r in rows]


def delete_show(show_id: str) -> bool:
    """Delete a show. Returns True if it existed."""
    with _get_conn() as conn:
        cursor = conn.execute("DELETE FROM shows WHERE id = ?", (show_id,))
        return cursor.rowcount > 0


def get_show_count() -> int:
    """Return total number of shows in the catalog."""
    with _get_conn() as conn:
        row = conn.execute("SELECT COUNT(*) as cnt FROM shows").fetchone()
        return row["cnt"]


def _row_to_show(row: sqlite3.Row) -> ShowInfo:
    features_data = json.loads(row["features_json"]) if row["features_json"] != "{}" else None
    features = ScriptFeatures(**features_data) if features_data else None
    return ShowInfo(
        id=row["id"],
        title=row["title"],
        year=row["year"],
        network=row["network"] or "",
        num_episodes_analyzed=row["num_episodes_analyzed"] or 0,
        features=features,
    )
