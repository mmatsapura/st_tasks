# Сценарий "Заказать":
#   1) товар - ТОЛЬКО inline: Пицца / Суши / Бургер
#      (callback_data: item:pizza и т.п.). Свободный текст на этом шаге
#      не принимай: "Нажми кнопку с товаром", state не меняй.
#   2) количество - целое число от 1 до 5; иначе останься на шаге.
#   3) адрес - не короче 5 символов.
#   4) телефон - только цифры, длина 10–13.
#   5) подтверждение - reply-кнопки "Да" / "Нет".
#      "Нет" - clear() и главное меню, заказ НЕ сохранять.
#      "Да" - сохранить в словарь по telegram_id (это уже не FSM),
#      показать сводку, clear(), главное меню.
#
# /start - клавиатура: "Заказать", "Мой заказ", "Отмена".
# "Мой заказ" - последняя СОХРАНЁННАЯ заявка из словаря, не черновик FSM.
#    Нет записи - "Заказов ещё не было".
# "Отмена" и /cancel - сбросить только FSM (черновик). Словарь заказов не трогать.
# Повторное "Заказать", если в словаре уже есть заказ - всё равно новая анкета;
# при "Да" она ПЕРЕЗАПИШЕТ старый заказ.
#
# Токен из BOT_TOKEN. Один файл, без БД.
# Ловушка на абракадабру - только когда state пустой (как StateFilter(None) в примере)..
#_______________________________________________________________________________________
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
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())



logging.basicConfig(level=logging.INFO)
router = Router()

foods = {'pizza': 'Пица',
         'sushi': 'Суши',
         'burger': 'Бургер'
         }

USER_ORDERS: dict[int, dict] = {}


def format_order(data: dict) -> str:
    return (
        f'Блюдо: {data["product"]}\n'
        f'Количество: {data["quantity"]}\n'
        f'Адрес доставки: {data["address"]}\n'
        f'Номер телефона: {data["phone_number"]}'
    )


class PlaceOrder(StatesGroup):
    product = State()
    quantity = State()
    address = State()
    phone_number = State()
    confirmation = State()


def main_keyboard() ->ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Заказать')],
            [KeyboardButton(text='Мой заказ')],
            [KeyboardButton(text='Отмена')],
        ],
        resize_keyboard=True
    )


def items_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=title, callback_data=f'food:{key}')]
            for key, title in foods.items()
        ]
    )


def confirmation_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Да')],
            [KeyboardButton(text='Нет')]
        ],
        resize_keyboard=True
    )


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(text='Выберите действие:', reply_markup=main_keyboard())


@router.message(Command('cancel'))
@router.message(F.text == 'Отмена')
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        await message.answer('Отменять нечего.', reply_markup=main_keyboard())
        return

    await state.clear()
    await message.answer('Текущий процесс оформления отменен.',
                         reply_markup=main_keyboard())


@router.message(F.text == 'Заказать', StateFilter(None))
async def order_start(message: Message, state: FSMContext) -> None:
    await state.set_state(PlaceOrder.product)
    await message.answer('Меню:', reply_markup=ReplyKeyboardRemove())
    await message.answer('Выберите блюдо:', reply_markup=items_keyboard())


@router.message(F.text == 'Мой заказ')
async def my_order_info(message: Message) -> None:
    order_data = USER_ORDERS.get(message.from_user.id)
    if order_data:
        await message.answer('Ваш заказ:\n' + format_order(order_data))
    else:
        await message.answer('Заказов еще не было.')


@router.callback_query(PlaceOrder.product, F.data.startswith('food:'))
async def chosen_product(callback: CallbackQuery, state: FSMContext) -> None:
    key = callback.data.split(':', 1)[1]
    title = foods.get(key)
    if title is None:
        await callback.answer('Не найдено!')
        return
    await callback.answer('Done!')
    await state.update_data(product=title)
    await state.set_state(PlaceOrder.quantity)
    await callback.message.answer('Какое количество желаете?')


@router.message(PlaceOrder.product, F.text)
async def ignore_text_product(message: Message) -> None:
    await message.answer('Пожалуйста, нажми на кнопку с товаром.')


@router.message(PlaceOrder.quantity, F.text)
async def process_quantity(message: Message, state: FSMContext) -> None:
    if not message.text.isdigit():
        await message.answer('Введите цифры от 1 до 5')
        return
    quantity = int(message.text)
    if not 1 <= quantity <=5:
        await message.answer('Введите цифры от 1 до 5')
        return
    await state.update_data(quantity=quantity)
    await state.set_state(PlaceOrder.address)
    await message.answer('Куда оформить доставку?')


@router.message(PlaceOrder.address, F.text)
async def process_address(message: Message, state: FSMContext) -> None:
    if not len(message.text.strip()) >= 5:
        await message.answer('Адрес должен быть не короче 5 символов')
        return
    address = message.text
    await state.update_data(address=address)
    await state.set_state(PlaceOrder.phone_number)
    await message.answer('Укажите номер телефона')


@router.message(PlaceOrder.phone_number, F.text)
async def process_phone_number(message: Message, state: FSMContext) -> None:
    if not message.text.isdigit() or not 10 <= len(message.text) <= 13:
        await message.answer('Номер телефона должен быть только из цифр, длина 10–13')
        return
    phone_number = message.text
    await state.update_data(phone_number=phone_number)
    await state.set_state(PlaceOrder.confirmation)
    data = await state.get_data()
    await message.answer(f'Подтвердите ваш заказ:\n {format_order(data)}', reply_markup=confirmation_keyboard())


@router.message(PlaceOrder.confirmation, F.text == 'Нет')
async def process_answer_no(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer('Заказ отменен', reply_markup=main_keyboard())


@router.message(PlaceOrder.confirmation, F.text == 'Да')
async def process_answer_yes(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    USER_ORDERS[message.from_user.id] = data
    await state.clear()
    await message.answer(
        'Заказ сохранен.\n' + format_order(data),
        reply_markup=main_keyboard(),
    )


@router.message(PlaceOrder.confirmation, F.text)
async def process_confirm_other(message: Message) -> None:
    await message.answer('Выбери «Да» или «Нет».')


@router.message(StateFilter(None), F.text)
async def other(message: Message) -> None:
    await message.answer('Нажми /start')


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