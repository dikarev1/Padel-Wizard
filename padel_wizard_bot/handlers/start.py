"""Handlers responsible for the /start entry point."""
from __future__ import annotations

import logging

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message

from padel_wizard_bot.keyboards.questionnaire import build_question_keyboard
from padel_wizard_bot.services.questionnaire_flow import DEFAULT_FLOW
from padel_wizard_bot.states.questionnaire import QuestionnaireStates

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
                    text="Launch the wizard",
                    callback_data="wizard_launch",
                )
            ]
        ]
    )

    await message.answer(
        (
            "Hello!\n\n"
            "This is Padel Wizard. Tap the button below to go on with the questionnaire."
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
    else:
        logger.info("'Начать опросник' button pressed by an unknown user")

    message = callback.message
    if message is None:
        await callback.answer()
        return

    first_question = DEFAULT_FLOW.get_question(DEFAULT_FLOW.first_question_id)

    await state.set_state(QuestionnaireStates.waiting_for_answer)
    await state.update_data(
        current_question_id=first_question.id,
        answers=[],
    )

    keyboard = build_question_keyboard(first_question)

    await message.answer(
        first_question.text,
        reply_markup=keyboard.as_markup(),
    )
    await callback.answer()
