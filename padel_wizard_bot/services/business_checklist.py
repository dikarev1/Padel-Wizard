"""Helpers for sending and tracking Telegram Business checklists."""
from __future__ import annotations

import logging
from typing import Any, Dict, Iterable, List, Tuple

from aiogram import Bot


logger = logging.getLogger(__name__)


HITS_CHECKLIST_QUESTION_ID = "hits_checklist"

HITS_CHECKLIST_TASKS: Tuple[Tuple[str, str], ...] = (
    ("hit_forehand", "+ Форхенд"),
    ("hit_backhand", "+ Бэкхенд"),
    ("hit_volley_lob", "+ Воллей, лоб"),
    ("hit_backhand_volley", "+ Бэкхенд-воллей, полуволлей"),
    ("hit_bandeja_smash", "+ Ранняя бандежa, ранний смэш, смэш x4"),
    ("hit_bajada_vibora", "+ Бахада, ранняя вибора"),
    ("hit_gancho_chiquita", "+ Ранний ганчо/руло, чикита, укороченный удар"),
    ("hit_spin_control", "+ Сильный контроль вращения"),
    ("hit_full_arsenal", "Почти весь доступный арсенал паделя с множеством формаций"),
)


def build_checklist_tasks_payload(tasks: Iterable[Tuple[str, str]]) -> List[Dict[str, str]]:
    """Convert internal task tuples to the payload format."""

    return [{"id": task_id, "text": text} for task_id, text in tasks]


async def send_hits_checklist(bot: Bot, business_connection_id: str, chat_id: int) -> Dict[str, Any]:
    """Send the hits checklist via raw Telegram Business API call."""

    url = f"https://api.telegram.org/bot{bot.token}/sendChecklist"

    tasks_payload = build_checklist_tasks_payload(HITS_CHECKLIST_TASKS)
    payload = {
        "business_connection_id": business_connection_id,
        "chat_id": chat_id,
        "checklist": {
            "tasks": tasks_payload,
        },
    }

    async with bot.session.post(url, json=payload) as response:
        response_data = await response.json()

    if not response_data.get("ok"):
        logger.warning("Failed to send hits checklist: %s", response_data)

    result = response_data.get("result") or {}
    return {
        "api_response": response_data,
        "tasks": tasks_payload,
        "message_id": result.get("message_id"),
    }
