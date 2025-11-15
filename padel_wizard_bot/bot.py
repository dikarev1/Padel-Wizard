from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher

from padel_wizard_bot.config import settings
from padel_wizard_bot.logging_config import setup_logging
from padel_wizard_bot.handlers import questionnaire, start


setup_logging(settings.log_level)
logger = logging.getLogger(__name__)


def create_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher()
    dispatcher.include_router(start.router)
    dispatcher.include_router(questionnaire.router)
    return dispatcher


async def main() -> None:
    bot_token = settings.bot_token
    if not bot_token:
        logger.critical(
            "Bot token is not configured. Set the BOT_TOKEN environment variable or update the .env file.",
        )
        raise RuntimeError("Missing bot token")

    bot = Bot(bot_token)
    dispatcher = create_dispatcher()
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
