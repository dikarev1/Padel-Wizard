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


<<<<<<< HEAD
async def main() -> None:
    bot_token = settings.bot_token
    if not bot_token:
        logger.critical(
            "Bot token is not configured. Set the BOT_TOKEN environment variable or update the .env file.",
=======
LANGUAGE_NAMES = {
    "ru": "Русский / Russian",
    "en": "English / Английский",
}


@dp.message(CommandStart())
async def cmd_start(message: Message):
    user = message.from_user
    if user:
        logger.info(
            "User %s opened the bot via /start",
            f"id={user.id}, username={user.username!r}"
>>>>>>> 18b6e848c15cdbbe37ad611049b769cbbd45f61e
        )
        raise RuntimeError("Missing bot token")

<<<<<<< HEAD
    bot = Bot(bot_token)
    dispatcher = create_dispatcher()
    await dispatcher.start_polling(bot)
=======
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=LANGUAGE_NAMES["ru"],
                    callback_data="lang_ru"
                ),
                InlineKeyboardButton(
                    text=LANGUAGE_NAMES["en"],
                    callback_data="lang_en"
                )
            ]
        ]
    )

    await message.answer(
        "Пожалуйста, выберите язык общения. / Please choose your preferred language.",
        reply_markup=keyboard
    )
    if user:
        logger.info(
            "Sent language selection keyboard to %s",
            f"id={user.id}, username={user.username!r}"
        )
    else:
        logger.info("Sent language selection keyboard to an unknown user")


@dp.callback_query(F.data.in_({"lang_ru", "lang_en"}))
async def on_language_chosen(callback: CallbackQuery):
    language_code = callback.data.split("_")[-1]
    language_label = LANGUAGE_NAMES.get(language_code, "unknown")

    user = callback.from_user
    if user:
        logger.info(
            "User %s selected language %s",
            f"id={user.id}, username={user.username!r}",
            language_label
        )
    else:
        logger.info("Language selected by an unknown user: %s", language_label)

    message = callback.message
    if message is None:
        logger.warning(
            "Callback without message for language selection from user %s",
            user.id if user else "unknown"
        )
        await callback.answer()
        return

    wizard_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Запустить мастер / Launch the wizard",
                    callback_data=f"wizard_launch:{language_code}"
                )
            ]
        ]
    )

    await message.answer(
        (
            f"Вы выбрали язык: {language_label}.\n"
            "Нажмите кнопку ниже, чтобы запустить опросник. / "
            "Tap the button below to start the questionnaire."
        ),
        reply_markup=wizard_keyboard
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("wizard_launch:"))
async def on_wizard_launch(callback: CallbackQuery):
    language_code = callback.data.split(":", 1)[-1]
    language_label = LANGUAGE_NAMES.get(language_code, "unknown")
    user = callback.from_user
    if user:
        logger.info(
            "User %s pressed 'Launch the wizard' (%s)",
            f"id={user.id}, username={user.username!r}",
            language_label
        )
    else:
        logger.info("'Launch the wizard' button pressed by an unknown user (%s)", language_label)

    message = callback.message
    if message is None:
        logger.warning(
            "Callback without message for wizard launch from user %s",
            user.id if user else "unknown"
        )
        await callback.answer()
        return

    options_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Играю хорошо / Playing well",
                    callback_data=f"playing_well:{language_code}"
                ),
                InlineKeyboardButton(
                    text="Играю плохо / Playing badly",
                    callback_data=f"playing_badly:{language_code}"
                )
            ]
        ]
    )

    await message.answer(
        (
            "Отлично, начинаем опросник. / Great, let's begin the questionnaire.\n\n"
            "Как вы сегодня играете? / How are you playing today?"
        ),
        reply_markup=options_keyboard
    )
    if user:
        logger.info(
            "Presented playing state options to %s (%s)",
            f"id={user.id}, username={user.username!r}",
            language_label
        )
    else:
        logger.info("Presented playing state options to an unknown user (%s)", language_label)
    await callback.answer()


@dp.callback_query(F.data.startswith(("playing_well", "playing_badly")))
async def on_playing_state_chosen(callback: CallbackQuery):
    language_code = callback.data.split(":", 1)[-1] if ":" in callback.data else "unknown"
    language_label = LANGUAGE_NAMES.get(language_code, "unknown")
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
        logger.warning(
            "Callback without message for playing state from user %s",
            user.id if user else "unknown"
        )
        await callback.answer()
        return

    await message.answer(
        "Спасибо за прохождение опроса! / Thanks for finishing the wizard!"
    )
    if user:
        logger.info(
            "Wizard finished for %s after selecting %s (%s)",
            f"id={user.id}, username={user.username!r}",
            callback.data,
            language_label
        )
    else:
        logger.info(
            "Wizard finished for an unknown user with state %s (%s)",
            callback.data,
            language_label
        )
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
>>>>>>> 18b6e848c15cdbbe37ad611049b769cbbd45f61e


if __name__ == "__main__":
    asyncio.run(main())
