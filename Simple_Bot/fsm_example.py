
import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

logging.basicConfig(level=logging.INFO)
router = Router()

DIRECTIONS = {
    "yoga": "Йога",
    "box": "Бокс",
    "run": "Бег",
}

# Сохранённые анкеты. Не путать с FSM.
PROFILES: dict[int, dict] = {}


class Registration(StatesGroup):
    direction = State()
    name = State()
    age = State()
    confirm = State()


def main_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Анкета"), KeyboardButton(text="Моя анкета")],
            [KeyboardButton(text="Отмена")],
        ],
        resize_keyboard=True,
    )


def directions_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=title, callback_data=f"dir:{key}")]
            for key, title in DIRECTIONS.items()
        ]
    )


def confirm_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Да"), KeyboardButton(text="Нет")]],
        resize_keyboard=True,
    )


def format_profile(data: dict) -> str:
    return (
        f"Направление: {data['direction']}\n"
        f"Имя: {data['name']}\n"
        f"Возраст: {data['age']}"
    )


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "Клуб. «Анкета» — черновик из четырёх шагов.\n"
        "Без FSM я бы не отличил имя от возраста и от кнопки «Да».",
        reply_markup=main_keyboard(),
    )


@router.message(Command("cancel"))
@router.message(F.text == "Отмена")
async def cmd_cancel(message: Message, state: FSMContext) -> None:
    if await state.get_state() is None:
        await message.answer("Черновик пуст. Сохранённую анкету не трогаю.")
        return
    await state.clear()
    await message.answer("Черновик сброшен.", reply_markup=main_keyboard())


@router.message(F.text == "Моя анкета")
async def my_profile(message: Message) -> None:
    saved = PROFILES.get(message.from_user.id)
    if not saved:
        await message.answer("Сохранённой анкеты ещё нет.")
        return
    await message.answer("Последняя сохранённая:\n" + format_profile(saved))


@router.message(F.text == "Анкета")
async def start_form(message: Message, state: FSMContext) -> None:
    await state.set_state(Registration.direction)
    await message.answer(
        "Выбери направление кнопкой, не текстом.",
        reply_markup=ReplyKeyboardRemove(),
    )
    await message.answer("Направления:", reply_markup=directions_keyboard())


@router.message(Registration.direction, F.text)
async def direction_text_rejected(message: Message) -> None:
    await message.answer("Нажми кнопку с направлением.")


@router.callback_query(Registration.direction, F.data.startswith("dir:"))
async def direction_chosen(callback: CallbackQuery, state: FSMContext) -> None:
    key = callback.data.split(":", 1)[1]
    title = DIRECTIONS.get(key)
    await callback.answer()
    if title is None:
        await callback.message.answer("Нет такого направления.")
        return
    await state.update_data(direction=title)
    await state.set_state(Registration.name)
    await callback.message.answer("Как тебя зовут? Не короче 2 букв.")


@router.message(Registration.name, F.text)
async def process_name(message: Message, state: FSMContext) -> None:
    name = message.text.strip()
    if len(name) < 2:
        await message.answer("Имя слишком короткое, ещё раз.")
        return
    await state.update_data(name=name)
    await state.set_state(Registration.age)
    await message.answer(f"Ок, {name}. Сколько полных лет? Число 10–100.")


@router.message(Registration.age, F.text)
async def process_age(message: Message, state: FSMContext) -> None:
    if not message.text.isdigit():
        await message.answer("Нужна цифра. Направление и имя я уже помню.")
        return
    age = int(message.text)
    if age < 10 or age > 100:
        await message.answer("Возраст от 10 до 100.")
        return
    await state.update_data(age=age)
    data = await state.get_data()
    await state.set_state(Registration.confirm)
    await message.answer(
        "Проверь черновик:\n" + format_profile(data) + "\nСохранить?",
        reply_markup=confirm_keyboard(),
    )


@router.message(Registration.confirm, F.text == "Да")
async def confirm_yes(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    PROFILES[message.from_user.id] = data
    await state.clear()
    await message.answer(
        "Сохранил в словарь, не в FSM.\n" + format_profile(data),
        reply_markup=main_keyboard(),
    )


@router.message(Registration.confirm, F.text == "Нет")
async def confirm_no(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Не сохраняю.", reply_markup=main_keyboard())


@router.message(Registration.confirm, F.text)
async def confirm_other(message: Message) -> None:
    await message.answer("Нажми «Да» или «Нет».")


@router.message(StateFilter(None), F.text)
async def unknown(message: Message) -> None:
    await message.answer("Нажми «Анкета» или /start.")


async def main() -> None:
    token = os.getenv("TOKEN")
    if not token:
        raise RuntimeError("Задай переменную окружения BOT_TOKEN")
    bot = Bot(token=token)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
