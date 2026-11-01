from aiogram.types import CallbackQuery

from database import USER_DATA, USER_LIMITS, USER_CATEGORIES


def format_response(data: dict) -> str:
    return (
        f'Транзакция №{data['transaction_number']}\n'
        f'Сумма: {data['amount_money']}\n'
        f'Тип транзакции: {data['transaction_type']}\n'
        f'Категория: {data['category']}\n'
        f'Время транзакции: {data['date']}'
    )


def get_day(user_id, date) -> float|int:
    total = 0.0
    transactions = USER_DATA.get(user_id, [])
    for item in transactions:
        if item['date'][:10] == date and item['transaction_type'] == 'Расходы💸':
            total += float(item['amount_money'])
    return total

def get_month(user_id, date) -> float|int:
    total = 0.0
    transactions = USER_DATA.get(user_id, [])
    for item in transactions:
        if item['date'][3:10] == date and item['transaction_type'] == 'Расходы💸':
            total += float(item['amount_money'])
    return total


def get_balance(user_id) -> float|int:
    total_income = 0
    total_expenses = 0
    transactions = USER_DATA.get(user_id, [])
    for item in transactions:
        if item['transaction_type'] == 'Доходы🤑':
            total_income += float(item['amount_money'])
        elif item['transaction_type'] == 'Расходы💸':
            total_expenses += float(item['amount_money'])
    total = total_income - total_expenses
    return round(total, 2)


def get_expenses_by_category(user_id) -> dict:
    category_totals = {}
    transactions = USER_DATA.get(user_id, [])
    for item in transactions:
        if item['transaction_type'] == 'Расходы💸':
            if item['category'] not in category_totals:
                category_totals[item['category']] = float(item['amount_money'])
            else:
                category_totals[item['category']] += float(item['amount_money'])
    return category_totals


def set_limit_month(user_id, limit_name, amount) -> None:
    if user_id not in USER_LIMITS:
        USER_LIMITS[user_id] = {}
    USER_LIMITS[user_id][limit_name] = amount


def set_limit_category(user_id, category, amount) -> None:
    if user_id not in USER_LIMITS:
        USER_LIMITS[user_id] = {}
    USER_LIMITS[user_id][category] = amount


def get_button_text(callback: CallbackQuery) -> str:
    keyboard = callback.message.reply_markup
    if keyboard and keyboard.inline_keyboard:
        for row in keyboard.inline_keyboard:
            for button in row:
                if button.callback_data == callback.data:
                    return button.text
    return callback.data