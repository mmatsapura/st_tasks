# # Задание: Telegram-бот с викториной
#
# ## 1. Главное меню
#
# При команде /start покажи клавиатуру:
#
# | Играть | Рекорд |
#
# | Помощь | Отмена |
#
# - Играть - запускает викторину из трёх вопросов.
# - Рекорд - показывает лучший результат пользователя или "Рекорда ещё нет".
# - Помощь и /help - объясняют правила игры.
# - Отмена и /cancel - прерывают игру.
#
# ## 2. Состояния и хранение данных
#
# Создай три состояния FSM: question_1, question_2, question_3.
#
# При старте игры сохрани score = 0 через state.update_data().
#
# Для рекордов используй глобальный словарь SCORES, где ключ - telegram_id, а значение - лучший результат пользователя. Рекорды хранятся только до перезапуска бота.
#
# ## 3. Вопросы викторины
#
# ### Вопрос 1 - Inline-кнопки
#
# Сколько байт в одном килобайте в двоичной системе измерения?
#
# Варианты: 1000, 1024, 8.
#
# - callback_data: q1:1000, q1:1024, q1:8.
# - Правильный ответ - 1024, за него начисляется 1 очко.
# - На любое текстовое сообщение отвечай: "Выбери вариант кнопкой".
# - При нажатии обязательно вызывай callback.answer().
#
# ### Вопрос 2 - Текстовый ответ
#
# Сколько ног у паука? Напиши число.
#
# - Ответ 8 - начисли 1 очко.
# - Любое другое число - 0 очков за вопрос, но переходи дальше.
# - Если введено не число, попроси повторить ответ. Состояние и счёт не меняй.
#
# ### Вопрос 3 - Inline-кнопки
#
# Какой оператор в Python проверяет равенство двух значений?
#
# Варианты: =, ==, ===.
#
# - callback_data: q3:assign, q3:eq, q3:js.
# - Правильный ответ - q3:eq, за него начисляется 1 очко.
# - На текст отвечай: "Выбери вариант кнопкой".
# - При нажатии обязательно вызывай callback.answer().
#
# ## 4. Завершение игры
#
# После третьего ответа:
#
# 1. Покажи итог: "Твой счёт: N/3".
# 2. Если рекорда нет или результат выше предыдущего, обнови SCORES и сообщи: "Новый рекорд: N".
# 3. Очисти FSM через await state.clear().
#
# Кнопка "Рекорд" должна показывать только сохранённый рекорд, а не текущий счёт игры.
#
# ## 5. Отмена и неизвестные сообщения
#
# - /cancel и кнопка "Отмена" очищают FSM, но не изменяют SCORES.
# - Если активной игры нет, ответь: "Нечего отменять".
# - При отмене активной игры сообщи: "Игра отменена".
# - Неизвестные сообщения вне игры обрабатывай через StateFilter(None) и отвечай: "Нажми Играть или /start".
#_______________________________________________________________________________________
import asyncio
import logging
import os

from aiogram import Router, Bot, Dispatcher, F
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())


logging.basicConfig(level=logging.INFO)

router = Router()

SCORES: dict[int, dict] = {}


quiz_1 = {'1000': '1000',
          '1024': '1024',
          '8': '8'
         }

quiz_3 = {'=': '=',
          '==': '==',
          '===': '==='
         }

class Questions(StatesGroup):
    question_1 = State()
    question_2 = State()
    question_3 = State()


def main_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Играть'), KeyboardButton(text='Рекорд')],
            [KeyboardButton(text='Помощь'), KeyboardButton(text='Отмена')]
        ],
        resize_keyboard=True
    )


def quiz1_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=title, callback_data=f'quiz1:{key}')]
            for key, title in quiz_1.items()
        ]
    )


def quiz3_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=title, callback_data=f'quiz3:{key}')]
            for key, title in quiz_3.items()
        ]
    )


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer('Главное меню:', reply_markup=main_keyboard())


@router.message(Command('cancel'))
@router.message(F.text == 'Отмена')
async def cmd_cancel(message: Message, state: FSMContext) -> None:
    current_game = await state.get_state()
    if not current_game:
        await message.answer('Нечего отменять')
        return
    await message.answer('Игра отменена')
    await state.clear()


@router.message(F.text == 'Рекорд')
async def get_record(message: Message) -> None:
    record = SCORES.get(message.from_user.id)
    if record is not None:
        await message.answer(f'Рекорд: {record}')
    else:
        await message.answer('Рекордов еще не было.')


@router.message(Command('help'))
@router.message(F.text == 'Помощь')
async def get_info(message: Message) -> None:
    await message.answer('Дай максимальное количество верных ответов и поставь новый рекорд.\nУ тебя получится!')



@router.message(F.text == 'Играть', StateFilter(None))
async def start_play(message: Message, state: FSMContext) -> None:
    await state.set_state(Questions.question_1)
    await state.update_data(score=0)
    await message.answer('Вопрос №1:\nСколько байт в одном килобайте в двоичной системе измерения?', reply_markup=quiz1_keyboard())


@router.callback_query(Questions.question_1, F.data.startswith('quiz1:'))
async def play_quiz_1(callback: CallbackQuery, state: FSMContext) -> None:
    key = callback.data.split(':', 1)[1]
    answer = quiz_1.get(key)
    data = await state.get_data()
    current_score = data.get('score', 0)
    if answer =='1024':
        current_score += 1
        await callback.message.answer('Отлично..Ответ верный!')
    else:
        await callback.message.answer('Упс..Ошибочка')
    await state.update_data(score= current_score, question_1=answer)
    await state.set_state(Questions.question_2)
    await callback.answer()
    await callback.message.answer('Вопрос №2:\nСколько ног у паука? Напиши число:')


@router.message(Questions.question_1, F.text)
async def ignore_text_question_1(message: Message) -> None:
    await message.answer('Выбери вариант кнопкой')


@router.message(Questions.question_2, F.text)
async def play_quiz_2(message: Message, state: FSMContext) -> None:
    if not message.text.isdigit() or not message.text:
        await message.answer('Только цифры.Повтори ответ!')
        return
    data = await state.get_data()
    current_score = data.get('score', 0)
    if int(message.text) == 8:
        current_score += 1
        await message.answer('Отлично..Ответ верный!')
    else:
        await message.answer('Упс..Ошибочка')
    await state.update_data(score=current_score, question_2=message.text)
    await state.set_state(Questions.question_3)
    await message.answer('Вопрос №3:\nКакой оператор в Python проверяет равенство двух значений?', reply_markup=quiz3_keyboard())


@router.callback_query(Questions.question_3, F.data.startswith('quiz3:'))
async def play_quiz_3(callback: CallbackQuery, state: FSMContext) -> None:
    key = callback.data.split(':', 1)[1]
    answer = quiz_3.get(key)
    data = await state.get_data()
    current_score = data.get('score', 0)
    if answer == '==':
        current_score += 1
        await callback.message.answer('Отлично..Ответ верный!')
    else:
        await callback.message.answer('Упс..Ошибочка')
    await callback.answer()
    past_record = SCORES.get(callback.from_user.id)
    await callback.message.answer(f'Твой счёт {current_score}/3')
    if past_record is None or current_score > past_record:
        SCORES[callback.from_user.id] = current_score
        await callback.message.answer(f'Новый рекорд побит {current_score}!')
    await state.clear()


@router.message(Questions.question_3, F.text)
async def ignore_text_question_3(message: Message) -> None:
    await message.answer('Выбери вариант кнопкой')


@router.message(StateFilter(None))
async def other(message: Message) -> None:
    await message.answer('Нажми Играть или /start')


async def main() -> None:
    token = os.getenv('BOT_TOKEN')
    if not token:
        raise RuntimeError('Задай переменную окружения')
    bot = Bot(token=token)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())