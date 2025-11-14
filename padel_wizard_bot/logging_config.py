import logging
import logging.handlers
from pathlib import Path


def setup_logging(level: str = "INFO") -> None:
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

    # Консольный поток
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)

    # Файловый поток с ротацией
    file_handler = logging.handlers.RotatingFileHandler(
        log_dir / "bot.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)

    # Базовая настройка логгера
    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(level)
    root.addHandler(console_handler)
    root.addHandler(file_handler)

    # Чтобы aiogram не захламлял WARN логами
    logging.getLogger("aiogram.event").setLevel(logging.INFO)
    logging.getLogger("aiogram.dispatcher").setLevel(logging.INFO)
    logging.getLogger("aiohttp.access").setLevel(logging.WARNING)
