"""Handlers responsible for the /start entry point."""
from __future__ import annotations

import logging
from typing import Any

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message,
)

from padel_wizard_bot.handlers.question_sender import send_question
from padel_wizard_bot.services.questionnaire_flow import DEFAULT_FLOW
from padel_wizard_bot.states.questionnaire import QuestionnaireStates
from storage.repo import repository

router = Router()
logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    user = message.from_user
    if user:
        logger.info(
            "User %s opened the bot via /start",
            f"id={user.id}, username={user.username!r}",
        )
    else:
        logger.info("Bot opened via /start by an unknown user")

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Запустить Padel Wizard",
                    callback_data="wizard_launch",
                )
            ]
        ]
    )

    await message.answer(
        (
            "Привет! Я — <b>Padel Wizard</b> 🪄\n\n"
            "Я задам тебе <b>7–8 вопросов</b>, чтобы ты узнал свой уровень игры в падел и получил персональные советы для улучшения.\n\n"
            "Старайся отвечать честно - от этого зависит точность результата"
        ),
        reply_markup=keyboard,
    )


@router.callback_query(F.data == "wizard_launch")
async def on_wizard_launch(callback: CallbackQuery, state: FSMContext) -> None:
    user = callback.from_user
    if user:
        logger.info(
            "User %s pressed 'Начать опросник'",
            f"id={user.id}, username={user.username!r}",
        )
        try:
            session = await repository.start_session(user.id, user.username)
        except Exception:
            logger.exception(
                "Failed to start questionnaire session for user %s",
                f"id={user.id}, username={user.username!r}",
            )
            session = None
        else:
            logger.info(
                "Started session %s (internal id %s) for user %s",
                session.session_number,
                session.id,
                f"id={user.id}, username={user.username!r}",
            )
    else:
        logger.info("'Начать опросник' button pressed by an unknown user")
        session = None

    message = callback.message
    if not isinstance(message, Message):
        await callback.answer()
        return

    first_question = DEFAULT_FLOW.get_question(DEFAULT_FLOW.first_question_id)

    await state.set_state(QuestionnaireStates.waiting_for_answer)
    state_payload: dict[str, Any] = {
        "current_question_id": first_question.id,
        "answers": [],
    }
    if session is not None:
        state_payload["session_id"] = session.id
        state_payload["session_number"] = session.session_number

    await state.update_data(state_payload)

    await send_question(message, first_question)
    await callback.answer()
