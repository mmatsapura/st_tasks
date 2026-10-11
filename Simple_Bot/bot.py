import asyncio
import logging
import os
import random

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)

logging.basicConfig(level=logging.INFO)

router = Router()

FACTS = [
    "Вода закипает при 100°C.",
    "У осьминога три сердца.",
    "Бананы — ягоды, клубника — нет.",
]


def main_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Факт"), KeyboardButton(text="Кубик")],
            [KeyboardButton(text="Настроение"), KeyboardButton(text="Помощь")],
        ],
        resize_keyboard=True,
    )


def mood_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="😊 Хорошо", callback_data="mood:good"),
                InlineKeyboardButton(text="😐 Нормально", callback_data="mood:ok"),
            ],
            [InlineKeyboardButton(text="😔 Плохо", callback_data="mood:bad")],
        ]
    )


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    name = message.from_user.first_name if message.from_user else "друг"
    await message.answer(
        f"Привет, {name}! Я простой чат-бот.\n"
        "Жми кнопки внизу или пиши /help.",
        reply_markup=main_keyboard(),
    )


@router.message(Command("help"))
@router.message(F.text == "Помощь")
async def cmd_help(message: Message) -> None:
    await message.answer(
        "/start — меню\n"
        "/id — твой Telegram id\n"
        "Факт — случайный факт\n"
        "Кубик — число от 1 до 6\n"
        "Настроение — inline-кнопки"
    )


@router.message(Command("id"))
async def cmd_id(message: Message) -> None:
    user = message.from_user
    await message.answer(f"Твой id: {user.id}\nUsername: @{user.username or 'нет'}")


@router.message(F.text == "Факт")
async def send_fact(message: Message) -> None:
    await message.answer(random.choice(FACTS))


@router.message(F.text == "Кубик")
async def roll_dice(message: Message) -> None:
    await message.answer(f"Выпало: {random.randint(1, 6)}")


@router.message(F.text == "Настроение")
async def ask_mood(message: Message) -> None:
    await message.answer("Как дела?", reply_markup=mood_keyboard())


@router.callback_query(F.data.startswith("mood:"))
async def mood_chosen(callback: CallbackQuery) -> None:
    key = callback.data.split(":", 1)[1]
    replies = {
        "good": "Отлично, так держать!",
        "ok": "Нормально — тоже результат.",
        "bad": "Бывает. Завтра может быть легче.",
    }
    await callback.answer()
    await callback.message.answer(replies.get(key, "Не понял настроение"))





async def main() -> None:
    # token = os.getenv("BOT_TOKEN")
    # if not token:
    #     raise RuntimeError("Задай переменную окружения BOT_TOKEN")
    bot = Bot(token='')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
