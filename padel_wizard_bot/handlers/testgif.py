from __future__ import annotations

import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from padel_wizard_bot.handlers.question_sender import (
    AnimationSendResult,
    Q3_ANIMATION_CACHE,
    send_q3_animation,
)

logger = logging.getLogger(__name__)

router = Router()


@router.message(Command("testgif"))
async def cmd_testgif(message: Message) -> None:
    logger.info(
        "testgif: path=%s exists=%s",
        Q3_ANIMATION_CACHE.file_path,
        Q3_ANIMATION_CACHE.file_path.exists(),
    )
    result = await send_q3_animation(message)
    if result is AnimationSendResult.FILE_NOT_FOUND:
        await message.answer(
            "Файл GIF не найден по пути:\n%s" % Q3_ANIMATION_CACHE.file_path
        )
    elif result is AnimationSendResult.FAILED_TO_SEND:
        await message.answer("Ошибка при отправке GIF, смотри логи.")
