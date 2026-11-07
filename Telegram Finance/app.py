import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from handlers import router

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    token = os.getenv('BOT_TOKEN')
    if not token:
        raise RuntimeError('Задай переменную окружения BOT_TOKEN')
    bot = Bot(token=token)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())