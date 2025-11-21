"""Handlers that operate the questionnaire FSM."""
from __future__ import annotations

import logging
from typing import Any

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from padel_wizard_bot.keyboards.questionnaire import (
    FinalScreenCallback,
    build_question_keyboard,
    build_final_keyboard,
)
from padel_wizard_bot.handlers.start import cmd_start
from padel_wizard_bot.services.experience import calculate_player_experience
from padel_wizard_bot.services.final_rating import calculate_final_rating
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
            experience = calculate_player_experience(answers)
            if experience is not None:
                logger.info(
                    "Session %s experience calculated: q1=%.1f months, q2=%.1f months, total=%.1f months, level=%s",
                    session_id,
                    experience.q1_months,
                    experience.q2_months,
                    experience.total_months,
                    experience.level,
                )
                await repository.upsert_player_experience(
                    int(session_id),
                    q1_months=experience.q1_months,
                    q2_months=experience.q2_months,
                    total_months=experience.total_months,
                    primary_racket_sport=experience.primary_racket_sport,
                    experience_level=experience.level,
                )
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

        final_rating = calculate_final_rating(answers)
        if final_rating is not None:
            final_text = f"Спасибо! Твой рейтинг = **{final_rating.level}**"
            logger.info(
                "Final rating calculated: level=%s, score=%.2f, experience_level=%s, skills=%s",
                final_rating.level,
                final_rating.score,
                final_rating.experience_level,
                final_rating.skill_levels,
            )
        else:
            final_text = (
                "Спасибо! Это финальный экран-заглушка. Здесь появится результат и рекомендации."
            )

        await state.clear()
        final_keyboard = build_final_keyboard()
        await message.answer(
            final_text,
            reply_markup=ReplyKeyboardRemove(),
        )
        await message.answer(
            "Выберите действие:",
            reply_markup=final_keyboard.as_markup(),
        )
        if user:
            logger.info(
                "User %s saw the final screen", f"id={user.id}, username={user.username!r}"
            )
        else:
            logger.info("Final screen shown to unknown user")
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


@router.callback_query(FinalScreenCallback.filter())
async def on_final_screen_action(
    callback: CallbackQuery, callback_data: FinalScreenCallback, state: FSMContext
) -> None:
    user = callback.from_user
    action = callback_data.action
    if user:
        logger.info(
            "User %s pressed final screen action %s",
            f"id={user.id}, username={user.username!r}",
            action,
        )
    else:
        logger.info(
            "Final screen action %s triggered by unknown user", action
        )

    message = callback.message
    if message is None:
        await callback.answer()
        return

    if action == "restart":
        await state.clear()
        await cmd_start(message)
        await callback.answer("Опросник запущен заново")
        return

    await callback.answer()
    await message.answer("вот твои советы")
