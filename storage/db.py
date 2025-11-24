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
                questionnaire_completed INTEGER NOT NULL DEFAULT 0,
                final_rating TEXT,
                received_advice INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL
            )
            """
        )

        cursor = connection.execute("PRAGMA table_info(users)")
        existing_columns = {row[1] for row in cursor.fetchall()}
        if "username" not in existing_columns:
            connection.execute("ALTER TABLE users ADD COLUMN username TEXT")
        if "questionnaire_completed" not in existing_columns:
            connection.execute(
                "ALTER TABLE users ADD COLUMN questionnaire_completed INTEGER NOT NULL DEFAULT 0"
            )
        if "final_rating" not in existing_columns:
            connection.execute("ALTER TABLE users ADD COLUMN final_rating TEXT")
        if "received_advice" not in existing_columns:
            connection.execute(
                "ALTER TABLE users ADD COLUMN received_advice INTEGER NOT NULL DEFAULT 0"
            )

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_number INTEGER NOT NULL UNIQUE,
                user_id INTEGER NOT NULL,
                answers_json TEXT NOT NULL DEFAULT '[]',
                interim_rating REAL,
                finished INTEGER NOT NULL DEFAULT 0,
                final_level TEXT,
                started_at TEXT NOT NULL,
                finished_at TEXT,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """
        )

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS player_experiences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL UNIQUE,
                q1_months REAL NOT NULL,
                q2_months REAL NOT NULL,
                total_months REAL NOT NULL,
                primary_racket_sport TEXT,
                experience_level TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
            )
            """
        )

        cursor = connection.execute("PRAGMA table_info(player_experiences)")
        experience_columns = {row[1] for row in cursor.fetchall()}
        if "primary_racket_sport" not in experience_columns:
            connection.execute(
                "ALTER TABLE player_experiences ADD COLUMN primary_racket_sport TEXT"
            )
