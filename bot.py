import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

# ВРЕМЕННО: вставь сюда токен бота из BotFather
BOT_TOKEN = "8373154970:AAGYoJqSLU2Nak-BMoh9UDyYpjiim1J1Vrs"


bot = Bot(BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Hello, World!")


async def main():
    # long polling
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
