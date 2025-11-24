"""Shared helpers for sending questionnaire questions and media."""
from __future__ import annotations

import logging
from enum import Enum
from pathlib import Path

from aiogram.types import Message

from padel_wizard_bot.keyboards.questionnaire import build_question_keyboard
from padel_wizard_bot.services.media_cache import AnimationCache
from padel_wizard_bot.services.questionnaire_flow import Question

logger = logging.getLogger(__name__)


class AnimationSendResult(Enum):
    SENT = "sent"
    FILE_NOT_FOUND = "file_not_found"
    FAILED_TO_SEND = "failed_to_send"


def _resolve_q3_animation_path() -> Path:
    """Return an existing path for the q3 GIF, trying common locations.

    Preference order:
    1. ``padel_wizard_bot/services/3_q.gif`` (bundled alongside the code)
    2. ``services/3_q.gif`` in the project root (legacy location)
    """

    candidate_paths = [
        Path(__file__).resolve().parent.parent / "services" / "3_q.gif",
        Path(__file__).resolve().parents[2] / "services" / "3_q.gif",
    ]

    logger.info("Q3 path candidates: %s", candidate_paths)

    for path in candidate_paths:
        if path.exists():
            return path

    logger.warning("Q3 animation file not found in expected locations: %s", candidate_paths)
    return candidate_paths[0]


Q3_ANIMATION_CACHE = AnimationCache(_resolve_q3_animation_path())


async def send_q3_animation(message: Message) -> AnimationSendResult:
    logger.info(
        "Q3 animation lookup: path=%s exists=%s",
        Q3_ANIMATION_CACHE.file_path,
        Q3_ANIMATION_CACHE.file_path.exists(),
    )

    try:
        animation_input = Q3_ANIMATION_CACHE.get_input()
    except FileNotFoundError:
        logger.error("Q3 animation file is missing: %s", Q3_ANIMATION_CACHE.file_path)
        return AnimationSendResult.FILE_NOT_FOUND

    try:
        animation_message = await message.answer_animation(animation=animation_input)
    except Exception:
        logger.exception(
            "Failed to send animation for question q3 from %s",
            Q3_ANIMATION_CACHE.file_path,
        )
        return AnimationSendResult.FAILED_TO_SEND

    if animation_message.animation:
        Q3_ANIMATION_CACHE.remember(animation_message.animation.file_id)

    return AnimationSendResult.SENT


async def send_question(message: Message, question: Question) -> None:
    """Send question text and, for q3, an accompanying GIF."""

    keyboard = build_question_keyboard(question)
    await message.answer(
        question.text,
        reply_markup=keyboard.as_markup(resize_keyboard=True, one_time_keyboard=True),
    )

    if question.id == "q3":
        await send_q3_animation(message)
