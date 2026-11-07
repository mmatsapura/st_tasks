from aiogram.types import (InlineKeyboardButton,
                           InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton)
from constants import (choice_statistic, choice_type, choice_add_type,
                       choice_category_expenses, choice_limits, choice_del_or_edit, choice_edit)
from database import USER_CATEGORIES


def main_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Добавить транзакцию💰'), KeyboardButton(text='Статистика транзакций📊')],
            [KeyboardButton(text='История🕒'), KeyboardButton(text='Настройки⚙️')],
            [KeyboardButton(text='Информация по доступным командамℹ️')]
        ],
        resize_keyboard=True
    )


def category_transaction_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=title, callback_data=f'type:{key}')]
            for key, title in choice_type.items()
        ]
    )


def category_keyboard_income(user_id) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=title, callback_data=f'income_cat:{key}')]
            for key, title in USER_CATEGORIES.get(user_id, {}).items() if 'income' in key
        ]
    )


def category_keyboard_expenses(user_id) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=title, callback_data=f'expenses_cat:{key}')]
            for key, title in USER_CATEGORIES.get(user_id, {}).items() if 'expenses' in key
        ]
    )


def statistic_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=title, callback_data=f'statistic:{key}')]
            for key, title in choice_statistic.items()
        ]
    )


def limits_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=title, callback_data=f'limits:{key}')]
            for key, title in choice_limits.items()
        ]
    )


def limits_for_category_keyboard(user_id) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=title, callback_data=f'limits_category:{key}')]
            for key, title in USER_CATEGORIES.get(user_id, choice_category_expenses).items() if 'expenses' in key
        ]
    )


def create_category_type_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=title, callback_data=f'add_type:{key}')]
            for key, title in choice_add_type.items()
        ]
    )


def del_category_keyboard(user_id) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=title, callback_data=f'del_cat:{key}')]
            for key, title in USER_CATEGORIES.get(user_id, {}).items()
        ]
    )


def edit_category_keyboard(user_id) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=title, callback_data=f'edit_cat:{key}')]
            for key, title in USER_CATEGORIES.get(user_id, {}).items()
        ]
    )


def history_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=title, callback_data=f'history_del_edit:{key}')]
            for key, title in choice_del_or_edit.items()
        ]
    )


def edit_history_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=title, callback_data=f'edit_history:{key}')]
            for key, title in choice_edit.items()
        ]
    )


def change_history_category_keyboard(user_id) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=title, callback_data=f'edit_history:{key}')]
            for key, title in USER_CATEGORIES.get(user_id, {}).items()
        ]
    )