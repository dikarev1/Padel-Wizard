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

    if len(question.options) >= 3:
        builder.adjust(2)
    else:
        builder.adjust(1)

    return builder


class FinalScreenCallback(CallbackData, prefix="final"):
    """Callback payload for actions on the final screen."""

    action: str


class HitsChecklistCallback(CallbackData, prefix="hits"):
    """Callback payload for hits checklist related actions."""

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


def build_hits_completion_keyboard() -> InlineKeyboardBuilder:
    """Inline keyboard for completing the hits checklist step."""

    builder = InlineKeyboardBuilder()
    builder.button(
        text="Готово, показать результат",
        callback_data=HitsChecklistCallback(action="finish"),
    )
    builder.adjust(1)
    return builder
