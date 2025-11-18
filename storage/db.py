"""SQLite database helpers."""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Final


STORAGE_DIR: Final[Path] = Path(__file__).resolve().parent
DB_FILENAME: Final[str] = "padel_wizard.sqlite3"
DB_PATH: Final[Path] = STORAGE_DIR / DB_FILENAME


def get_database_path() -> Path:
    """Return the path to the SQLite database file."""
    return DB_PATH


def initialize_database() -> None:
    """Create the SQLite database and required tables if they do not exist."""
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON")

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER NOT NULL UNIQUE,
                username TEXT,
                created_at TEXT NOT NULL
            )
            """
        )

        cursor = connection.execute("PRAGMA table_info(users)")
        existing_columns = {row[1] for row in cursor.fetchall()}
        if "username" not in existing_columns:
            connection.execute("ALTER TABLE users ADD COLUMN username TEXT")

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_number INTEGER NOT NULL UNIQUE,
                user_id INTEGER NOT NULL,
                answers_json TEXT NOT NULL DEFAULT '[]',
                interim_rating REAL,
                experience_months REAL,
                experience_level TEXT,
                finished INTEGER NOT NULL DEFAULT 0,
                final_level TEXT,
                started_at TEXT NOT NULL,
                finished_at TEXT,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """
        )

        cursor = connection.execute("PRAGMA table_info(sessions)")
        existing_session_columns = {row[1] for row in cursor.fetchall()}
        if "experience_months" not in existing_session_columns:
            connection.execute("ALTER TABLE sessions ADD COLUMN experience_months REAL")
        if "experience_level" not in existing_session_columns:
            connection.execute("ALTER TABLE sessions ADD COLUMN experience_level TEXT")
