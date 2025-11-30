from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from padel_wizard_bot.config import settings
from padel_wizard_bot.handlers import errors, questionnaire, start, testgif
from padel_wizard_bot.logging_config import setup_logging


setup_logging(settings.log_level)
logger = logging.getLogger(__name__)


def create_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher()
    dispatcher.include_router(errors.router)
    dispatcher.include_router(start.router)
    dispatcher.include_router(questionnaire.router)
    dispatcher.include_router(testgif.router)
    return dispatcher


async def main() -> None:
    bot_token = settings.bot_token
    if not bot_token:
        logger.critical(
            "Bot token is not configured. Set the BOT_TOKEN environment variable or update the .env file.",
        )
        raise RuntimeError("Missing bot token")

    dispatcher = create_dispatcher()

    logger.info("Starting bot polling")
    try:
        async with Bot(
            bot_token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        ) as bot:
            await dispatcher.start_polling(bot)
    except Exception:
        logger.exception("Bot polling stopped due to an unexpected error")
        raise
    finally:
        logger.info("Bot polling stopped")


if __name__ == "__main__":
    asyncio.run(main())
