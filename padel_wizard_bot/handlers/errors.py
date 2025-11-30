"""Global error handler for logging unexpected failures during update processing."""
from __future__ import annotations

import logging
from typing import Optional

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import ErrorEvent, TelegramObject, Update

router = Router()
logger = logging.getLogger(__name__)


def _extract_user(update: Update) -> Optional[TelegramObject]:
    """Return the most relevant user object attached to the update."""

    if update.message and update.message.from_user:
        return update.message.from_user
    if update.callback_query and update.callback_query.from_user:
        return update.callback_query.from_user
    if update.inline_query and update.inline_query.from_user:
        return update.inline_query.from_user
    if update.chosen_inline_result and update.chosen_inline_result.from_user:
        return update.chosen_inline_result.from_user
    return None


def _extract_chat_id(update: Update) -> Optional[int]:
    """Return chat id if present for the update."""

    if update.message and update.message.chat:
        return update.message.chat.id
    if update.callback_query and update.callback_query.message:
        return update.callback_query.message.chat.id
    if update.edited_message and update.edited_message.chat:
        return update.edited_message.chat.id
    return None


def _extract_payload(update: Update) -> str:
    """Return a short description of the payload that triggered the update."""

    if update.message and update.message.text:
        return update.message.text
    if update.callback_query:
        data = update.callback_query.data
        return f"callback_data={data!r}" if data else "callback_query without data"
    if update.inline_query:
        return f"inline_query={update.inline_query.query!r}"
    return "<no textual payload>"


@router.errors()
async def log_error(event: ErrorEvent, state: FSMContext) -> None:
    """Log unhandled exceptions with as much context as possible."""

    update = event.update
    user = _extract_user(update) if update else None
    chat_id = _extract_chat_id(update) if update else None
    payload = _extract_payload(update) if update else "<no update>"

    try:
        fsm_state = await state.get_state()
        fsm_data = await state.get_data()
    except Exception:
        logger.exception("Failed to fetch FSM context while handling an error")
        fsm_state = None
        fsm_data = None

    logger.error(
        "Unhandled exception for update %s (user=%s, chat=%s, payload=%s, fsm_state=%s, fsm_data=%s)",
        getattr(update, "update_id", "<unknown>"),
        user,
        chat_id,
        payload,
        fsm_state,
        fsm_data,
        exc_info=event.exception,
    )

