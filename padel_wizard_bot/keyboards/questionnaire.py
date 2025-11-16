"""Inline keyboards for questionnaire flow."""
from __future__ import annotations

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from padel_wizard_bot.services.questionnaire_flow import Question


class QuestionnaireAnswerCallback(CallbackData, prefix="qa"):
    """Callback payload for questionnaire answers."""

    question_id: str
    option_id: str


def build_question_keyboard(question: Question) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for option in question.options:
        builder.button(
            text=option.text,
            callback_data=QuestionnaireAnswerCallback(
                question_id=question.id,
                option_id=option.id,
            ),
        )
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
