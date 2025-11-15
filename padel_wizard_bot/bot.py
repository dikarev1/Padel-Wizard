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
    if user:
        logger.info(
            "Sent wizard launch keyboard to %s",
            f"id={user.id}, username={user.username!r}"
        )
    else:
        logger.info("Sent wizard launch keyboard to an unknown user")


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
        logger.warning("Callback without message for wizard launch from user %s", user.id if user else "unknown")
        await callback.answer()
        return

    options_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Playing well",
                    callback_data="playing_well"
                ),
                InlineKeyboardButton(
                    text="Playing badly",
                    callback_data="playing_badly"
                )
            ]
        ]
    )

    await message.answer(
        "Great, let's begin the questionnaire.\n\n"
        "How are you playing today?",
        reply_markup=options_keyboard
    )
    if user:
        logger.info(
            "Presented playing state options to %s",
            f"id={user.id}, username={user.username!r}"
        )
    else:
        logger.info("Presented playing state options to an unknown user")
    await callback.answer()


@dp.callback_query(F.data.in_({"playing_well", "playing_badly"}))
async def on_playing_state_chosen(callback: CallbackQuery):
    user = callback.from_user
    if user:
        logger.info(
            "User %s selected %s",
            f"id={user.id}, username={user.username!r}",
            callback.data
        )
    else:
        logger.info("Playing state selected by an unknown user: %s", callback.data)

    message = callback.message
    if message is None:
        logger.warning("Callback without message for playing state from user %s", user.id if user else "unknown")
        await callback.answer()
        return

    await message.answer("Thanks for finishing the wizard!")
    if user:
        logger.info(
            "Wizard finished for %s after selecting %s",
            f"id={user.id}, username={user.username!r}",
            callback.data,
        )
    else:
        logger.info("Wizard finished for an unknown user with state %s", callback.data)
    await callback.answer()


async def main():
    logger.info("Starting bot polling")
    try:
        await dp.start_polling(bot)
    except Exception:
        logger.exception("Bot polling stopped due to an unexpected error")
        raise
    finally:
        logger.info("Bot polling stopped")


if __name__ == "__main__":
    asyncio.run(main())


