"""Reply keyboards for questionnaire flow."""
from __future__ import annotations

from aiogram.utils.keyboard import ReplyKeyboardBuilder

from padel_wizard_bot.services.questionnaire_flow import Question


def build_question_keyboard(question: Question) -> ReplyKeyboardBuilder:
    """Build a reply keyboard with one button per answer option."""

    builder = ReplyKeyboardBuilder()
    for option in question.options:
        builder.button(text=option.text)
    builder.adjust(1)
    return builder
