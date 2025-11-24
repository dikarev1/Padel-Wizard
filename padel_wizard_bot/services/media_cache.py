"""Utility helpers for reusing uploaded media without re-uploading files."""
from __future__ import annotations

from pathlib import Path
from typing import Optional, Union

from aiogram.types import FSInputFile


MediaInput = Union[FSInputFile, str]


class AnimationCache:
    """Caches Telegram ``file_id`` for a local animation file."""

    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path
        self._file_id: Optional[str] = None

    @property
    def file_path(self) -> Path:
        return self._file_path

    def get_input(self) -> MediaInput:
        """Return cached file_id or a fresh FSInputFile for upload."""

        if self._file_id:
            return self._file_id
        if not self._file_path.exists():
            raise FileNotFoundError(self._file_path)
        return FSInputFile(self._file_path)

    def remember(self, file_id: str) -> None:
        """Store the server-side file_id for reuse."""

        self._file_id = file_id
