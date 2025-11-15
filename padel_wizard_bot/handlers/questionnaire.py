"""Handlers that operate the questionnaire FSM."""
from __future__ import annotations

import logging
from typing import Any

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from padel_wizard_bot.keyboards.questionnaire import (
    QuestionnaireAnswerCallback,
    build_question_keyboard,
)
from padel_wizard_bot.services.questionnaire_flow import DEFAULT_FLOW
from padel_wizard_bot.states.questionnaire import QuestionnaireStates

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(
    QuestionnaireStates.waiting_for_answer,
    QuestionnaireAnswerCallback.filter(),
)
async def on_question_answer(
    callback: CallbackQuery,
    callback_data: QuestionnaireAnswerCallback,
    state: FSMContext,
) -> None:
    user = callback.from_user
    if user:
        logger.info(
            "User %s answered %s with option %s",
            f"id={user.id}, username={user.username!r}",
            callback_data.question_id,
            callback_data.option_id,
        )
    else:
        logger.info(
            "Question answered by an unknown user: %s -> %s",
            callback_data.question_id,
            callback_data.option_id,
        )

    message = callback.message
    if message is None:
        await callback.answer()
        return

    state_data = await state.get_data()
    current_question_id = state_data.get("current_question_id")
    if current_question_id != callback_data.question_id:
        await callback.answer(
            "Этот вопрос больше не активен. Пожалуйста, отвечайте на текущий вопрос.",
            show_alert=True,
        )
        return

    answers: list[dict[str, Any]] = list(state_data.get("answers", []))
    answers.append(
        {
            "question_id": callback_data.question_id,
            "option_id": callback_data.option_id,
        }
    )
    await state.update_data(answers=answers)

    next_question_id = DEFAULT_FLOW.resolve_next(
        current_question_id=callback_data.question_id,
        option_id=callback_data.option_id,
    )

    if next_question_id is None:
        if user:
            logger.info(
                "User %s completed questionnaire with answers %s",
                f"id={user.id}, username={user.username!r}",
                answers,
            )
        else:
            logger.info("Questionnaire completed by unknown user: %s", answers)
        await state.clear()
        await message.answer(
            "Спасибо! Это финальный экран-заглушка. Здесь появится результат и рекомендации.",
        )
        await callback.answer()
        return

    next_question = DEFAULT_FLOW.get_question(next_question_id)
    await state.update_data(
        current_question_id=next_question.id,
    )

    keyboard = build_question_keyboard(next_question)
    await message.answer(
        next_question.text,
        reply_markup=keyboard.as_markup(),
    )
    await callback.answer()
