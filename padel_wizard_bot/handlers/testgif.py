from __future__ import annotations

import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from padel_wizard_bot.handlers.question_sender import Q3_ANIMATION_CACHE

logger = logging.getLogger(__name__)

router = Router()


@router.message(Command("testgif"))
async def cmd_testgif(message: Message) -> None:
    logger.info(
        "testgif: path=%s exists=%s",
        Q3_ANIMATION_CACHE.file_path,
        Q3_ANIMATION_CACHE.file_path.exists(),
    )
    try:
        animation_input = Q3_ANIMATION_CACHE.get_input()
    except FileNotFoundError:
        logger.error("testgif: file not found: %s", Q3_ANIMATION_CACHE.file_path)
        await message.answer(
            "Файл MP4 не найден по пути:\n%s" % Q3_ANIMATION_CACHE.file_path
        )
        return

    try:
        await message.answer_animation(animation=animation_input)
    except Exception:
        logger.exception("testgif: failed to send animation")
        await message.answer("Ошибка при отправке GIF, смотри логи.")
