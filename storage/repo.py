"""Repository layer for reading and writing session data."""
from __future__ import annotations

import asyncio
import json
import secrets
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable, Iterable, Optional, cast

from .db import DB_PATH, initialize_database


@dataclass(slots=True)
class UserRecord:
    """Representation of a user stored in the database."""

    id: int
    telegram_id: int
    created_at: str


@dataclass(slots=True)
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

    async def get_or_create_user(self, telegram_id: int) -> UserRecord:
        """Return an existing user or create a new record if needed."""

        def operation(connection: sqlite3.Connection) -> UserRecord:
            cursor = connection.execute(
                "SELECT id, telegram_id, created_at FROM users WHERE telegram_id = ?",
                (telegram_id,),
            )
            row = cursor.fetchone()
            if row:
                return UserRecord(
                    id=row["id"],
                    telegram_id=row["telegram_id"],
                    created_at=row["created_at"],
                )

            now = datetime.now(timezone.utc).isoformat()
            cursor = connection.execute(
                "INSERT INTO users (telegram_id, created_at) VALUES (?, ?)",
                (telegram_id, now),
            )
            user_id = cursor.lastrowid
            assert user_id is not None, "SQLite cursor must provide lastrowid after insert"
            return UserRecord(
                id=cast(int, user_id),
                telegram_id=telegram_id,
                created_at=now,
            )

        return await self._run(operation)

    async def start_session(self, telegram_id: int) -> SessionRecord:
        """Create a new questionnaire session for the given Telegram user ID."""

        def operation(connection: sqlite3.Connection) -> SessionRecord:
            cursor = connection.execute(
                "SELECT id FROM users WHERE telegram_id = ?",
                (telegram_id,),
            )
            row = cursor.fetchone()
            if row:
                user_id = cast(int, row["id"])
            else:
                cursor = connection.execute(
                    "INSERT INTO users (telegram_id, created_at) VALUES (?, ?)",
                    (telegram_id, datetime.now(timezone.utc).isoformat()),
                )
                user_id = cursor.lastrowid
                assert user_id is not None, "SQLite cursor must provide lastrowid after insert"
                user_id = cast(int, user_id)

            session_number = self._generate_session_number(connection)
            now = datetime.now(timezone.utc).isoformat()
            cursor = connection.execute(
                (
                    "INSERT INTO sessions (session_number, user_id, answers_json, started_at, "
                    "updated_at) VALUES (?, ?, ?, ?, ?)"
                ),
                (session_number, user_id, json.dumps([], ensure_ascii=False), now, now),
            )
            session_id = cursor.lastrowid
            assert session_id is not None, "SQLite cursor must provide lastrowid after insert"
            session_id = cast(int, session_id)
            return SessionRecord(
                id=session_id,
                session_number=session_number,
                user_id=user_id,
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
                id=cast(int, row["id"]),
                session_number=cast(int, row["session_number"]),
                user_id=cast(int, row["user_id"]),
                answers=cast(list[dict[str, Any]], json.loads(row["answers_json"] or "[]")),
                interim_rating=cast(Optional[float], row["interim_rating"]),
                finished=bool(row["finished"]),
                final_level=cast(Optional[str], row["final_level"]),
                started_at=cast(str, row["started_at"]),
                finished_at=cast(Optional[str], row["finished_at"]),
                updated_at=cast(str, row["updated_at"]),
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
