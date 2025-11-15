import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from padel_wizard_bot.config import settings
from padel_wizard_bot.logging_config import setup_logging

setup_logging(settings.log_level)

logger = logging.getLogger(__name__)

bot_token = settings.bot_token
if not bot_token:
    logger.critical(
        "Bot token is not configured. Set the BOT_TOKEN environment variable or update the .env file."
    )
    raise RuntimeError("Missing bot token")

bot = Bot(bot_token)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    user = message.from_user
    if user:
        logger.info(
            "User %s opened the bot via /start",
            f"id={user.id}, username={user.username!r}"
        )
    else:
        logger.info("Bot opened via /start by an unknown user")

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Launch the wizard",
                    callback_data="wizard_launch"
                )
            ]
        ]
    )

    await message.answer(
        "Hello, World!\n\n"
        "This is Padel Wizard. Tap the button below to go on with the questionnaire.",
        reply_markup=keyboard
    )


@dp.callback_query(F.data == "wizard_launch")
async def on_wizard_launch(callback: CallbackQuery):
    user = callback.from_user
    if user:
        logger.info(
            "User %s pressed 'Начать опросник'",
            f"id={user.id}, username={user.username!r}"
        )
    else:
        logger.info("'Начать опросник' button pressed by an unknown user")

    message = callback.message
    if message is None:
        await callback.answer()
        return

    await message.answer("Great, let's begin the questionnaire.")
    await callback.answer()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())


