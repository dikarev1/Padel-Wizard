"""Handlers that operate the questionnaire FSM."""
from __future__ import annotations

import logging
from typing import Any, Dict, Iterable, List, Set

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove, Update

from padel_wizard_bot.keyboards.questionnaire import (
    FinalScreenCallback,
    HitsChecklistCallback,
    build_final_keyboard,
    build_hits_completion_keyboard,
    build_question_keyboard,
)
from padel_wizard_bot.handlers.start import cmd_start
from padel_wizard_bot.services.business_checklist import (
    HITS_CHECKLIST_QUESTION_ID,
    send_hits_checklist,
)
from padel_wizard_bot.services.questionnaire_flow import DEFAULT_FLOW
from padel_wizard_bot.states.questionnaire import QuestionnaireStates
from storage.repo import repository

router = Router()
logger = logging.getLogger(__name__)


async def _finalize_questionnaire(
    message: Message,
    state: FSMContext,
    answers: List[Dict[str, Any]],
    session_id: int | None,
    user: Any,
) -> None:
    if session_id is not None:
        try:
            await repository.mark_finished(int(session_id))
        except Exception:
            logger.exception("Failed to mark session %s as finished", session_id)

    await state.clear()
    final_keyboard = build_final_keyboard()
    await message.answer(
        "Спасибо! Это финальный экран-заглушка. Здесь появится результат и рекомендации.",
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


async def _persist_hits_selection(
    state: FSMContext,
    state_data: Dict[str, Any],
    selected_hits: Iterable[str],
) -> List[Dict[str, Any]]:
    ordered_hits = list(selected_hits)
    tasks_order: List[str] | None = state_data.get("hits_tasks_order")
    if tasks_order:
        ordered_hits = [text for text in tasks_order if text in set(selected_hits)]

    answers: List[Dict[str, Any]] = [
        item
        for item in list(state_data.get("answers", []))
        if item.get("question_id") != HITS_CHECKLIST_QUESTION_ID
    ]
    answers.append(
        {
            "question_id": HITS_CHECKLIST_QUESTION_ID,
            "selected_hits": ordered_hits,
        }
    )
    await state.update_data(answers=answers, selected_hits=ordered_hits)

    session_id = state_data.get("session_id")
    if session_id is not None:
        try:
            await repository.update_answers(int(session_id), answers)
        except Exception:
            logger.exception(
                "Failed to persist answers for session %s", session_id
            )

    user_id = state_data.get("user_id")
    if user_id is not None:
        try:
            await repository.save_hits(int(user_id), ordered_hits)
        except Exception:
            logger.exception("Failed to save hits for user %s", user_id)

    return answers


async def _start_hits_checklist(
    message: Message, state: FSMContext, question_text: str
) -> None:
    await state.set_state(QuestionnaireStates.waiting_for_hits_checklist)
    await state.update_data(current_question_id=HITS_CHECKLIST_QUESTION_ID)

    await message.answer(question_text, reply_markup=ReplyKeyboardRemove())

    state_data = await state.get_data()
    business_connection_id = state_data.get("business_connection_id")
    if not business_connection_id:
        logger.warning(
            "Cannot send hits checklist without business_connection_id for chat %s",
            message.chat.id,
        )
        await message.answer(
            "Не удалось получить business_connection_id. Свяжитесь с ботом через Telegram Business, чтобы отправить чек-лист.",
            reply_markup=build_hits_completion_keyboard().as_markup(),
        )
        return

    try:
        checklist_info = await send_hits_checklist(
            bot=message.bot,
            business_connection_id=str(business_connection_id),
            chat_id=message.chat.id,
        )
    except Exception:
        logger.exception(
            "Failed to send hits checklist for chat %s", message.chat.id
        )
        await message.answer(
            "Не удалось отправить чек-лист ударов. Попробуйте снова позже или завершите опрос.",
            reply_markup=build_hits_completion_keyboard().as_markup(),
        )
        return

    tasks_payload = checklist_info.get("tasks", [])
    tasks_map = {task["id"]: task["text"] for task in tasks_payload if "id" in task}
    tasks_order = [task["text"] for task in tasks_payload if "text" in task]
    payload_to_store: Dict[str, Any] = {
        "hits_tasks_map": tasks_map,
        "hits_tasks_order": tasks_order,
    }
    if checklist_info.get("message_id") is not None:
        payload_to_store["checklist_message_id"] = checklist_info["message_id"]

    await state.update_data(payload_to_store)

    await message.answer(
        "Отметьте подходящие удары в чек-листе. Когда будете готовы, нажмите кнопку ниже.",
        reply_markup=build_hits_completion_keyboard().as_markup(),
    )
    user = message.from_user
    if user:
        logger.info(
            "User %s received hits checklist", f"id={user.id}, username={user.username!r}"
        )
    else:
        logger.info("Hits checklist sent to unknown user")


@router.update()
async def on_business_connection(update: Update, state: FSMContext) -> None:
    if update.business_connection:
        await state.update_data(business_connection_id=update.business_connection.id)


@router.update()
async def on_checklist_update(update: Update, state: FSMContext) -> None:
    checklist_update = update.checklist_tasks_done
    if not checklist_update:
        return

    current_state = await state.get_state()
    if current_state != QuestionnaireStates.waiting_for_hits_checklist.state:
        return

    state_data = await state.get_data()
    if state_data.get("current_question_id") != HITS_CHECKLIST_QUESTION_ID:
        return

    tasks_map: Dict[str, str] = state_data.get("hits_tasks_map", {})
    selected_hits: Set[str] = set(state_data.get("selected_hits", []))

    for task in checklist_update.tasks:
        text = getattr(task, "text", None)
        if text is None and getattr(task, "task_id", None) is not None:
            text = tasks_map.get(task.task_id)

        if not text:
            continue

        if task.is_done:
            selected_hits.add(text)
        else:
            selected_hits.discard(text)

    tasks_order: List[str] | None = state_data.get("hits_tasks_order")
    selected_hits_in_order = (
        [text for text in tasks_order if text in selected_hits]
        if tasks_order
        else list(selected_hits)
    )

    state_data["selected_hits"] = selected_hits_in_order
    await state.update_data(selected_hits=selected_hits_in_order)

    user_id = state_data.get("user_id")
    if user_id is not None:
        try:
            await repository.save_hits(int(user_id), list(selected_hits))
        except Exception:
            logger.exception(
                "Failed to save hits for user %s after checklist update", user_id
            )

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
        await _finalize_questionnaire(message, state, answers, session_id, user)
        return

    if next_question_id == HITS_CHECKLIST_QUESTION_ID:
        hits_question = DEFAULT_FLOW.get_question(next_question_id)
        await _start_hits_checklist(message, state, hits_question.text)
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


@router.callback_query(HitsChecklistCallback.filter())
async def on_hits_checklist_action(
    callback: CallbackQuery, callback_data: HitsChecklistCallback, state: FSMContext
) -> None:
    message = callback.message
    if message is None:
        await callback.answer()
        return

    if callback_data.action != "finish":
        await callback.answer()
        return

    current_state = await state.get_state()
    if current_state != QuestionnaireStates.waiting_for_hits_checklist.state:
        await callback.answer("Сейчас чек-лист недоступен")
        return

    state_data = await state.get_data()
    selected_hits = state_data.get("selected_hits", [])

    answers = await _persist_hits_selection(state, state_data, selected_hits)
    session_id = state_data.get("session_id")
    user = callback.from_user

    if user:
        logger.info(
            "User %s finished hits checklist with %s",
            f"id={user.id}, username={user.username!r}",
            selected_hits,
        )
    else:
        logger.info("Hits checklist finished by unknown user: %s", selected_hits)

    await _finalize_questionnaire(message, state, answers, session_id, user)
    await callback.answer("Опрос завершён")


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
