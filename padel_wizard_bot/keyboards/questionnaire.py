"""Reply keyboards for questionnaire flow."""
from __future__ import annotations

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from padel_wizard_bot.services.questionnaire_flow import Question


def build_question_keyboard(question: Question) -> ReplyKeyboardBuilder:
    """Build a reply keyboard with one button per answer option."""

    builder = ReplyKeyboardBuilder()
    for option in question.options:
        builder.button(text=option.text)

    if question.id in {"q4", "q5", "q6"}:
        builder.adjust(1)
    elif len(question.options) >= 3:
        builder.adjust(2)
    else:
        builder.adjust(1)

    return builder


class FinalScreenCallback(CallbackData, prefix="final"):
    """Callback payload for actions on the final screen."""

    action: str


def build_final_keyboard() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Пройти опросник заново",
        callback_data=FinalScreenCallback(action="restart"),
    )
    builder.button(
        text="Получить советы для моего уровня",
        callback_data=FinalScreenCallback(action="advice"),
    )
    builder.adjust(1)
    return builder
