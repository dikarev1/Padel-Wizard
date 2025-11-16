import logging
import logging.handlers
from pathlib import Path
from typing import Union


def _normalize_level(level: Union[str, int]) -> int:
    """Convert logging level values to an integer supported by logging."""

    if isinstance(level, int):
        return level

    if isinstance(level, str):
        resolved_level = logging.getLevelName(level.upper())
        if isinstance(resolved_level, int):
            return resolved_level

    raise ValueError(f"Unsupported log level: {level!r}")


def setup_logging(level: Union[str, int] = "INFO") -> None:
    """
    Настраивает логирование для бота.
    Использует два потока: файл и консоль.
    Логи хранятся в logs/bot.log с ротацией.
    """

    # Создаем папку logs, если ее нет
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Общий формат логов
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    numeric_level = _normalize_level(level)

    # Консольный поток
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(numeric_level)

    # Файловый поток с ротацией
    file_handler = logging.handlers.RotatingFileHandler(
        log_dir / "bot.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(numeric_level)

    # Базовая настройка логгера
    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(numeric_level)
    root.addHandler(console_handler)
    root.addHandler(file_handler)

    # Чтобы aiogram не захламлял WARN логами
    logging.getLogger("aiogram.event").setLevel(logging.INFO)
    logging.getLogger("aiogram.dispatcher").setLevel(logging.INFO)
    logging.getLogger("aiohttp.access").setLevel(logging.WARNING)
