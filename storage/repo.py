"""Repository layer for reading and writing session data."""
from __future__ import annotations

import asyncio
import json
import secrets
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable, Iterable, Optional

from .db import DB_PATH, initialize_database


@dataclass
class UserRecord:
    """Representation of a user stored in the database."""

    id: int
    telegram_id: int
    username: Optional[str]
    created_at: str


@dataclass
class SessionRecord:
    """Representation of a questionnaire session."""

    id: int
    session_number: int
    user_id: int
    answers: list[dict[str, Any]]
    interim_rating: Optional[float]
    finished: bool
    final_level: Optional[str]
    started_at: str
    finished_at: Optional[str]
    updated_at: str


class StorageRepository:
    """High-level API for working with questionnaire sessions."""

    def __init__(self) -> None:
        initialize_database()

    async def _run(self, operation: Callable[[sqlite3.Connection], Any]) -> Any:
        """Execute a blocking SQLite operation in a thread pool."""

        def wrapper() -> Any:
            with sqlite3.connect(DB_PATH) as connection:
                connection.row_factory = sqlite3.Row
                connection.execute("PRAGMA foreign_keys = ON")
                result = operation(connection)
                connection.commit()
                return result

        return await asyncio.to_thread(wrapper)

    async def get_or_create_user(
        self, telegram_id: int, username: Optional[str] = None
    ) -> UserRecord:
        """Return an existing user or create a new record if needed."""

        def operation(connection: sqlite3.Connection) -> UserRecord:
            cursor = connection.execute(
                "SELECT id, telegram_id, username, created_at FROM users WHERE telegram_id = ?",
                (telegram_id,),
            )
            row = cursor.fetchone()
            if row:
                stored_username = username if username is not None else row["username"]
                if stored_username is not None and row["username"] != stored_username:
                    connection.execute(
                        "UPDATE users SET username = ? WHERE telegram_id = ?",
                        (stored_username, telegram_id),
                    )
                if username is not None and row["username"] != username:
                    stored_username = username
                return UserRecord(
                    id=row["id"],
                    telegram_id=row["telegram_id"],
                    username=stored_username,
                    created_at=row["created_at"],
                )

            now = datetime.now(timezone.utc).isoformat()
            cursor = connection.execute(
                "INSERT INTO users (telegram_id, username, created_at) VALUES (?, ?, ?)",
                (telegram_id, username, now),
            )
            user_id = cursor.lastrowid
            if user_id is None:
                raise RuntimeError("Failed to insert user: lastrowid is None")
            return UserRecord(
                id=user_id, telegram_id=telegram_id, username=username, created_at=now
            )

        return await self._run(operation)

    async def start_session(
        self, telegram_id: int, username: Optional[str] = None
    ) -> SessionRecord:
        """Create a new questionnaire session for the given Telegram user ID."""

        user = await self.get_or_create_user(telegram_id, username)

        def operation(connection: sqlite3.Connection) -> SessionRecord:
            if user.id is None:
                raise RuntimeError("Failed to get user_id: user.id is None")

            session_number = self._generate_session_number(connection)
            now = datetime.now(timezone.utc).isoformat()
            cursor = connection.execute(
                (
                    "INSERT INTO sessions (session_number, user_id, answers_json, started_at, "
                    "updated_at) VALUES (?, ?, ?, ?, ?)"
                ),
                (
                    session_number,
                    user.id,
                    json.dumps([], ensure_ascii=False),
                    now,
                    now,
                ),
            )
            session_id = cursor.lastrowid
            if session_id is None:
                raise RuntimeError("Failed to insert session: lastrowid is None")
            return SessionRecord(
                id=session_id,
                session_number=session_number,
                user_id=user.id,
                answers=[],
                interim_rating=None,
                finished=False,
                final_level=None,
                started_at=now,
                finished_at=None,
                updated_at=now,
            )

        return await self._run(operation)

    async def update_answers(
        self,
        session_id: int,
        answers: Iterable[dict[str, Any]],
    ) -> None:
        """Persist the provided answers for the given session."""

        answers_json = json.dumps(list(answers), ensure_ascii=False)
        timestamp = datetime.now(timezone.utc).isoformat()

        def operation(connection: sqlite3.Connection) -> None:
            connection.execute(
                "UPDATE sessions SET answers_json = ?, updated_at = ? WHERE id = ?",
                (answers_json, timestamp, session_id),
            )

        await self._run(operation)

    async def save_hits(self, user_id: int, hits: Iterable[str]) -> None:
        """Persist the selected hits list for the user."""

        hits_json = json.dumps(list(hits), ensure_ascii=False)
        timestamp = datetime.now(timezone.utc).isoformat()

        def operation(connection: sqlite3.Connection) -> None:
            connection.execute(
                (
                    "INSERT INTO user_hits (user_id, hits_json, updated_at) "
                    "VALUES (?, ?, ?) "
                    "ON CONFLICT(user_id) DO UPDATE SET "
                    "hits_json = excluded.hits_json, updated_at = excluded.updated_at"
                ),
                (user_id, hits_json, timestamp),
            )

        await self._run(operation)

    async def set_interim_rating(self, session_id: int, rating: float) -> None:
        """Store the latest interim rating value for the session."""

        timestamp = datetime.now(timezone.utc).isoformat()

        def operation(connection: sqlite3.Connection) -> None:
            connection.execute(
                "UPDATE sessions SET interim_rating = ?, updated_at = ? WHERE id = ?",
                (rating, timestamp, session_id),
            )

        await self._run(operation)

    async def mark_finished(
        self,
        session_id: int,
        *,
        finished: bool = True,
        final_level: Optional[str] = None,
    ) -> None:
        """Mark the session as finished and optionally store the final level."""

        timestamp = datetime.now(timezone.utc).isoformat()
        finished_at = timestamp if finished else None

        def operation(connection: sqlite3.Connection) -> None:
            connection.execute(
                (
                    "UPDATE sessions SET finished = ?, final_level = COALESCE(?, final_level), "
                    "finished_at = ?, updated_at = ? WHERE id = ?"
                ),
                (int(finished), final_level, finished_at, timestamp, session_id),
            )

        await self._run(operation)

    async def get_session(self, session_id: int) -> Optional[SessionRecord]:
        """Fetch a session record by its internal identifier."""

        def operation(connection: sqlite3.Connection) -> Optional[SessionRecord]:
            cursor = connection.execute(
                (
                    "SELECT id, session_number, user_id, answers_json, interim_rating, finished, "
                    "final_level, started_at, finished_at, updated_at FROM sessions WHERE id = ?"
                ),
                (session_id,),
            )
            row = cursor.fetchone()
            if row is None:
                return None
            return SessionRecord(
                id=row["id"],
                session_number=row["session_number"],
                user_id=row["user_id"],
                answers=json.loads(row["answers_json"] or "[]"),
                interim_rating=row["interim_rating"],
                finished=bool(row["finished"]),
                final_level=row["final_level"],
                started_at=row["started_at"],
                finished_at=row["finished_at"],
                updated_at=row["updated_at"],
            )

        return await self._run(operation)

    def _generate_session_number(self, connection: sqlite3.Connection) -> int:
        """Generate a random session number ensuring uniqueness."""

        while True:
            candidate = secrets.randbelow(10**12)
            cursor = connection.execute(
                "SELECT 1 FROM sessions WHERE session_number = ?",
                (candidate,),
            )
            if cursor.fetchone() is None:
                return candidate


repository = StorageRepository()
