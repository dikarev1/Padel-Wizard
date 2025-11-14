import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "8373154970:AAGYoJqSLU2Nak-BMoh9UDyYpjiim1J1Vrs"

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Launch the wizard",      # здесь можно поменять текст кнопки
                    callback_data="wizard_launch"  # внутренний идентификатор
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
    # Здесь позже начнем сам опросник
    await callback.message.answer("Great, let's begin the questionnaire.")
    await callback.answer()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
