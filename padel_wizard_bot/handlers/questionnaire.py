"""Handlers that operate the questionnaire FSM."""
from __future__ import annotations

import logging
from typing import Any

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from padel_wizard_bot.keyboards.questionnaire import build_question_keyboard
from padel_wizard_bot.services.questionnaire_flow import DEFAULT_FLOW
from padel_wizard_bot.states.questionnaire import QuestionnaireStates
from storage.repo import repository

router = Router()
logger = logging.getLogger(__name__)


@router.message(QuestionnaireStates.waiting_for_answer)
async def on_question_answer(message: Message, state: FSMContext) -> None:
    user = message.from_user
    state_data = await state.get_data()
    current_question_id = state_data.get("current_question_id")

    if current_question_id is None:
        await state.clear()
        await message.answer(
            "Опросник ещё не запущен. Нажмите кнопку запуска, чтобы начать."
        )
        return

    question = DEFAULT_FLOW.get_question(str(current_question_id))
    user_answer = (message.text or "").strip()

    option = next(
        (opt for opt in question.options if opt.text == user_answer), None
    )
    if option is None:
        await message.answer(
            "Пожалуйста, выберите один из вариантов с клавиатуры ниже."
        )
        return

    if user:
        logger.info(
            "User %s answered %s with option %s",
            f"id={user.id}, username={user.username!r}",
            question.id,
            option.id,
        )
    else:
        logger.info(
            "Question answered by an unknown user: %s -> %s",
            question.id,
            option.id,
        )

    answers: list[dict[str, Any]] = list(state_data.get("answers", []))
    answers.append(
        {
            "question_id": question.id,
            "option_id": option.id,
        }
    )
    await state.update_data(answers=answers)

    session_id = state_data.get("session_id")
    if session_id is not None:
        try:
            await repository.update_answers(int(session_id), answers)
        except Exception:
            logger.exception(
                "Failed to persist answers for session %s", session_id
            )

    next_question_id = DEFAULT_FLOW.resolve_next(
        current_question_id=question.id,
        option_id=option.id,
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
        if session_id is not None:
            try:
                await repository.mark_finished(int(session_id))
            except Exception:
                logger.exception(
                    "Failed to mark session %s as finished", session_id
                )

        await state.clear()
        await message.answer(
            "Спасибо! Это финальный экран-заглушка. Здесь появится результат и рекомендации.",
            reply_markup=ReplyKeyboardRemove(),
        )
        return

    next_question = DEFAULT_FLOW.get_question(next_question_id)
    await state.update_data(
        current_question_id=next_question.id,
    )

    keyboard = build_question_keyboard(next_question)
    await message.answer(
        next_question.text,
        reply_markup=keyboard.as_markup(resize_keyboard=True, one_time_keyboard=True),
    )
