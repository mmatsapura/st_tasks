# ТЗ: бот погоды в ОДНОМ файле
# httpx + json-файл + dataclass.
# Токен из BOT_TOKEN. pip: aiogram, httpx.
#
# Reply-клавиатура после /start:
#   Погода | Город
#   История | Помощь
#
# /help и «Помощь» - коротко, что умеет бот.
# Любой другой текст - последним хендлером: «Нажми кнопку меню, я простой бот.»
#
# «Город» - inline ≥ 4 городов (ключ, название, lat, lon).
# callback_data: city:kyiv. Сохрани город для telegram_id в JSON.
# callback.answer() обязателен. Пока не выбирали - Киев (или первый в списке).
#
# «Погода» - async GET Open-Meteo (без ключа):
#   https://api.open-meteo.com/v1/forecast
#   params: latitude, longitude, current=temperature_2m,weather_code, timezone=auto
#   timeout 10 сек.
# Ответ вида: «Киев: 12.4°C». Сначала dataclass, потом текст - не сырой dict.
# Ошибка сети/JSON - «Не удалось получить погоду», бот не падает.
#
# JSON рядом со скриптом (pathlib): выбранный город по id + последние 5 успешных
# запросов (город, температура, время). Нет файла / битый JSON  пустое состояние.
# «История» - эти 5 строк или «Истории пока нет».
# То есть нужен файл json с историей запросов
#
# Проверь: кнопки, inline, абракадабру, рестарт (город жив),
# без интернета — текст ошибки.
#_______________________________________________________________________________________
import datetime
import logging
import asyncio
import httpx
import os
import json

from pathlib import Path
from dataclasses import dataclass
from aiogram import Router, F, Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardMarkup, ReplyKeyboardMarkup, \
    KeyboardButton, InlineKeyboardButton, CallbackQuery

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())


logging.basicConfig(level=logging.INFO)
router = Router()

JSON_PATH = Path('users.json')
try:
    with open(JSON_PATH, 'r', encoding='utf-8') as filee:
        user_cities = json.load(filee)
except (FileNotFoundError, json.JSONDecodeError):
    user_cities = {}



CITIES = {
    "kyiv": ("Киев", 50.45, 30.52),
    "london": ("Лондон", 51.51, -0.13),
    "tokyo": ("Токио", 35.68, 139.69),
    "newyork": ("Нью-Йорк", 40.71, -74.01),
}


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(reply_markup=main_reply_keyboard(), text='Меню бота:')


def main_reply_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Погода'), KeyboardButton(text='Город')],
            [KeyboardButton(text='История'), KeyboardButton(text='Помощь')]
        ],
        resize_keyboard=True,
    )


@router.message(Command('help'))
@router.message(F.text == 'Помощь')
async def cmd_help(message: Message) -> None:
    await message.answer(
        '/start - меню\n'
        '/city - выбрать город\n'
        '/weather - узнать погоду\n'    
        '/history - история вызовов\n'
        '/help - справочник'
    )


@router.message(Command('city'))
@router.message(F.text == 'Город')
async def cmd_city(message: Message) -> None:
    await message.answer(reply_markup=city_inline_keyboard(),text='Выбери город:')


def city_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Киев', callback_data='city:kyiv')],
            [InlineKeyboardButton(text='Лондон', callback_data='city:london')],
            [InlineKeyboardButton(text='Токио', callback_data='city:tokyo')],
            [InlineKeyboardButton(text='Нью-Йорк', callback_data='city:newyork')],
        ]
    )


@router.callback_query(F.data.startswith('city:'))
async def city_chosen(callback: CallbackQuery) -> None:
    city_key = callback.data.split(':', 1)[1]
    user_id = str(callback.from_user.id)
    user_data = user_cities.get(user_id, {'history': []})
    user_data['city'] = city_key
    user_cities[user_id] = user_data
    with open(JSON_PATH, 'w') as file:
        json.dump(user_cities, file)
    await callback.answer()
    await callback.message.answer(CITIES.get(city_key, ['Не понял про какой город идет речь'])[0])


@router.message(Command('weather'))
@router.message(F.text == 'Погода')
async def cmd_weather(message: Message):
    user_id = str(message.from_user.id)
    user_data = user_cities.get(user_id, {'city': 'kyiv', 'history': []})
    city = user_data['city']
    try:
        weather_data = await get_weather_info(city)
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        history_record = {
            'city': weather_data.city,
            'temperature': weather_data.temperature,
            'time': current_time
        }
        user_data['history'].append(history_record)
        user_data['history'] = user_data['history'][-5:]
        user_cities[user_id] = user_data
        with open(JSON_PATH, 'w') as file:
            json.dump(user_cities, file)
        await message.answer(f'{weather_data.city}: {weather_data.temperature}°C')
    except Exception:
        await message.answer('Не удалось получить погоду')


@dataclass
class Weather:
    city: str
    temperature: float|int


async def get_weather_info(city_key) -> Weather:
    async with httpx.AsyncClient() as client:
        response = await client.get('https://api.open-meteo.com/v1/forecast',params = {
                                        'current': 'temperature_2m,weather_code',
                                        'timezone': 'auto',
                                        'latitude':CITIES[city_key][1],
                                        'longitude': CITIES[city_key][2],},
                                        timeout=10
                                    )
        data = response.json()
        return Weather(city=CITIES[city_key][0], temperature=data['current']['temperature_2m'])


@router.message(Command('history'))
@router.message(F.text == 'История')
async def cmd_history(message: Message) -> None:
    user_id = str(message.from_user.id)
    user_data = user_cities.get(user_id, {})
    history_list = user_data.get('history', [])
    if not history_list:
        await message.answer('Истории пока нет')
        return
    text = 'История запросов:\n'
    for item in history_list:
        text += f'{item['city']}: {item['temperature']}°C ({item['time']})\n'
    await message.answer(text)

@router.message()
async def all_text(message: Message) -> None:
    await message.answer('Нажми кнопку меню, я простой бот!')


async def main() -> None:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("Задай переменную окружения BOT_TOKEN")
    bot = Bot(token=token)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())