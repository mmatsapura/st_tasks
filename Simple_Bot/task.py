# Задание: простой бот «Мини-кафе» в ОДНОМ файле (как bot.py).
# Не нужны service / repository / несколько папок.
#
# Сделай бота, который:
# 1. На /start здоровается и показывает reply-клавиатуру:
#    «Меню», «Часы», «Контакты»
# 2. «Меню» — список из 3 напитков (название + цена текстом).
# 3. «Часы» — время работы (любая строка, например 9:00–21:00).
# 4. «Контакты» — адрес или телефон (любая строка).
# 5. После «Меню» покажи inline-кнопки с названиями тех же 3 напитков.
#    По нажатию бот пишет: «Ты выбрал: … Цена: …»
#    Не забудь callback.answer().
# 6. /help или кнопка «Помощь» (добавь на клавиатуру, если хочешь) —
#    коротко объяснить, что умеет бот.
# 7. Любой другой текст — «Нажми кнопку меню, я простой бот».
#    Этот handler должен быть ПОСЛЕДНИМ, иначе перехватит кнопки.
#
# Подсказки:
# - Кнопка reply и F.text == "Меню" должны совпадать буква в букву.
# - Inline: callback_data короткий, например drink:latte.
# - Токен — из BOT_TOKEN, не вписывай его в код.
#
# Когда запустишь: проверь /start, все кнопки, inline и «абракадабру» в чат.

#_______________________________________________________________________________________

import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,)

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())


logging.basicConfig(level=logging.INFO)

router = Router()


drinks = {'Tea': ('Чай', '20'), 'Coffee': ('Кофе', '30'), 'Water': ('Вода', '17')}


def main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
          [KeyboardButton(text='Меню'), KeyboardButton(text='Часы')],
            [KeyboardButton(text='Контакты'), KeyboardButton(text='Помощь')]
        ],
        resize_keyboard=True,
    )


def menu_keyboard():
    buttons = [
        [InlineKeyboardButton(text=name, callback_data=f'drink: {key}')]
        for key, (name, price) in drinks.items()
        ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.message(CommandStart())
async def cmd_start(message: Message):
    name = message.from_user.first_name if message.from_user else ' Незнакомец'
    await message.answer(
        f'Приветствую тебя {name}!',
        reply_markup=main_keyboard()
    )


@router.message(Command('menu'))
@router.message(F.text == 'Меню')
async def get_drinks(message: Message):
    menu_text = 'Меню:\n'
    for key, (name, price) in drinks.items():
        menu_text += f'{name} — {price}\n'
    await message.answer(menu_text, reply_markup=menu_keyboard())


@router.message(Command('time'))
@router.message(F.text == 'Часы')
async def get_work_time(message: Message):
    await message.answer('Мы работаем с понедельника по пятницу, рабочие часы 9:00-21:00')


@router.message(Command('contacts'))
@router.message(F.text == 'Контакты')
async def get_contact(message: Message):
    await message.answer('Адрес: ул. Владимира Винниченко, 14, Киев, 04053\n'
                         'Телефон: +380 44 234 56 78 ')


@router.message(Command('help'))
@router.message(F.text == 'Помощь')
async def get_info(message: Message):
    await message.answer('Доступные команды:\n'
                         ' /menu : Меню\n'
                         '/time : Время работы\n'
                         '/contacts : Наши контакты\n'
                         '/help : Посмотреть доступные команды')


@router.message()
async def get_rest(message: Message):
    await message.answer('Нажми кнопку меню или вызови команду /menu, я простой бот')


@router.callback_query(F.data.startswith('drink:'))
async def drink_chosen(callback: CallbackQuery):
    key = callback.data.split(':', 1)[1].strip()
    name, price = drinks[key]
    await callback.answer()
    await callback.message.answer(f'Вы выбрали: {name}. Цена: {price}')


async def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("Задай переменную окружения BOT_TOKEN")
    bot = Bot(token=token)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())