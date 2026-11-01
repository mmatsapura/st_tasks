from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from datetime import datetime
from aiogram.types import CallbackQuery, Message,ReplyKeyboardRemove
from aiogram import F, Router

from keyboards import (main_keyboard, statistic_keyboard, category_transaction_keyboard,
                       category_keyboard_expenses, category_keyboard_income, limits_keyboard,
                       limits_for_category_keyboard, create_category_type_keyboard,
                       del_category_keyboard, edit_category_keyboard,
                       history_keyboard, edit_history_keyboard,
                       change_history_category_keyboard)
from database import USER_DATA, TRANSACTION_ID, USER_LIMITS, USER_CATEGORIES
from constants import (choice_category_expenses, choice_category_income,
                       choice_type, choice_statistic)
from states import (StateStatistic, StateExpensesRevenue, StateSetAmount,
                    StateSetAmountCategory, StateCreateCategory, StateEditCategory,
                    StateDelTransaction, StateEditTransaction)
from services import (format_response, get_day, get_month, get_balance,
                      get_expenses_by_category, set_limit_month, set_limit_category, get_button_text)


router = Router()


@router.message(Command('menu'))
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    if user_id not in USER_CATEGORIES:
        USER_CATEGORIES[user_id] = choice_category_expenses|choice_category_income
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
    await message.answer('Текущий процесс отменен.',
                         reply_markup=main_keyboard())


@router.message(F.text == 'Добавить транзакцию💰', StateFilter(None))
async def add_transaction(message: Message, state: FSMContext) -> None:
    await state.set_state(StateExpensesRevenue.amount_money)
    await message.answer('Введите сумму:', reply_markup=ReplyKeyboardRemove())


@router.message(F.text == 'Статистика транзакций📊', StateFilter(None))
async def transaction_statistics(message: Message, state: FSMContext) -> None:
    await state.set_state(StateStatistic.statistics)
    await message.answer('Открываем раздел статистики...', reply_markup=ReplyKeyboardRemove())
    await message.answer('Выбери что хочешь посмотреть:', reply_markup=statistic_keyboard())


@router.callback_query(StateStatistic.statistics, F.data.startswith('statistic:'))
async def process_statistics(callback: CallbackQuery) -> None:
    await callback.answer()
    user_id = callback.from_user.id
    key = callback.data.split(':', 1)[1]
    title = choice_statistic.get(key)
    if title is None:
        await callback.message.answer('Не найдено!')
        return
    if key == 'one_day':
        date_day = datetime.now().strftime('%d.%m.%Y')
        await callback.message.answer(f'Расходы за день:\n{get_day(user_id, date_day)}')
    elif key == 'one_month':
        date_month = datetime.now().strftime('%m.%Y')
        await callback.message.answer(f'Расходы за месяц:\n{get_month(user_id, date_month)}')
    elif key == 'budget_balance':
        await callback.message.answer(f'Баланс за все время:\n{get_balance(user_id)}')
    elif key == 'status_limit':
        date_month = datetime.now().strftime('%m.%Y')
        user_limits = USER_LIMITS.get(user_id, {})
        limit = user_limits.get('total_budget', 0)
        expenses = get_month(user_id, date_month)
        balance = limit - expenses
        msg_text = (
            f'💰 Общий бюджет:\n'
            f'Лимит: {limit}\n'
            f'Потрачено: {expenses}\n'
            f'Остаток: {balance}\n\n'
            f'📊 Лимиты по категориям:\n'
        )
        for k, v in USER_LIMITS.get(user_id, {}).items():
            if not k == 'total_budget':
                user_cats = USER_CATEGORIES[user_id]
                category_name = user_cats.get(k, k)
                msg_text += f'{category_name}: {v}\n'
        await callback.message.answer(msg_text)
    elif key == 'expenses_by_category':
        text = 'Расходы по категориям:\n'
        categories_dict = get_expenses_by_category(user_id)
        if len(categories_dict) <= 0:
            await callback.message.answer('Расходов пока нет')
            await callback.answer()
            return
        for category, amount in categories_dict.items():
            text += f'{category}: {amount}\n'
        await callback.message.answer(text)



@router.message(StateExpensesRevenue.amount_money)
async def choice_type_transaction(message: Message, state: FSMContext) -> None:
    if not message.text.isdigit():
        await message.answer('Вводите только цифры')
        return
    await state.update_data(amount_money=int(message.text))
    await state.set_state(StateExpensesRevenue.transaction_type)
    await message.answer('Выберите категорию для распределения денежных средств:',
                         reply_markup=category_transaction_keyboard())


@router.callback_query(StateExpensesRevenue.transaction_type, F.data.startswith('type:'))
async def process_transaction_choice_type(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    key = callback.data.split(':', 1)[1]
    title = choice_type.get(key)
    user_id = callback.from_user.id
    if title is None:
        await callback.message.answer('Не найдено!')
        return
    await state.update_data(transaction_type=title)
    await state.set_state(StateExpensesRevenue.category)
    if key == 'income':
        await callback.message.answer('Выберите категорию:', reply_markup=category_keyboard_income(user_id))
    elif key == 'expenses':
        await callback.message.answer('Выберите категорию:', reply_markup=category_keyboard_expenses(user_id))


@router.callback_query(StateExpensesRevenue.category, F.data.startswith('income_cat:'))
async def process_income_category(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    key = callback.data.split(':', 1)[1]
    title = USER_CATEGORIES[callback.from_user.id].get(key)
    if title is None:
        await callback.message.answer('Не найдено!')
        return
    global TRANSACTION_ID
    TRANSACTION_ID += 1
    date_time = datetime.now().strftime('%d.%m.%Y %H:%M')
    await state.update_data(category=title, date=date_time, transaction_number=TRANSACTION_ID)
    data = await state.get_data()
    USER_DATA.setdefault(callback.from_user.id, []).append(data)
    await state.clear()
    await callback.message.answer('Добавлен доход:\n' + format_response(data), reply_markup=main_keyboard())


@router.callback_query(StateExpensesRevenue.category, F.data.startswith('expenses_cat:'))
async def process_expenses_category(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    user_id = callback.from_user.id
    key = callback.data.split(':', 1)[1]
    title = USER_CATEGORIES[user_id].get(key)
    if title is None:
        await callback.message.answer('Не найдено!')
        return
    global TRANSACTION_ID
    TRANSACTION_ID += 1
    date_time = datetime.now().strftime('%d.%m.%Y %H:%M')
    await state.update_data(category=title, date=date_time, transaction_number=TRANSACTION_ID)
    data = await state.get_data()
    USER_DATA.setdefault(user_id, []).append(data)
    user_limits = USER_LIMITS.get(user_id, {})
    limit = user_limits.get(key, 0)
    my_expenses = get_expenses_by_category(user_id)
    expenses = my_expenses.get(title, 0)
    if 0 < limit < expenses:
        await callback.message.answer('Расходы превышают лимит по категории️⚠️‼️')
    await state.clear()
    await callback.message.answer('Добавлен расход:\n' + format_response(data), reply_markup=main_keyboard())


@router.message(F.text == 'История🕒')
async def get_history(message: Message) -> None:
    last_transactions = USER_DATA.get(message.from_user.id, [])[-5:]
    text = 'Ваши последние операции:\n'
    if len(last_transactions) == 0:
        await message.answer('У вас пока нет истории операций')
    else:
        for item in last_transactions:
            id = item['transaction_number']
            cat = item['category']
            type = item['transaction_type']
            amount = item['amount_money']
            text += f'№{id} {type}: {cat} - {amount}\n'
        await message.answer(text, reply_markup=history_keyboard())


@router.callback_query(F.data == 'history_del_edit:del_transactions')
async def process_delete_transactions(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.set_state(StateDelTransaction.number)
    await callback.message.answer('Введите id транзакции которую хотите удалить:')


@router.message(StateDelTransaction.number, F.text)
async def del_category(message: Message, state: FSMContext) -> None:
    if not message.text.isdigit():
        await message.answer('Вводите только цифры!')
        return
    for item in USER_DATA[message.from_user.id]:
        if item['transaction_number'] == int(message.text):
            USER_DATA[message.from_user.id].remove(item)
            await message.answer('Транзакция успешно удалена ✅')
            await state.clear()
            return
    await message.answer('Транзакция с таким номером не найдена.')


@router.callback_query(F.data == 'history_del_edit:edit_transactions')
async def process_edit_transactions(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.set_state(StateEditTransaction.number)
    await callback.message.answer('Введите id транзакции которую хотите изменить:')


@router.message(StateEditTransaction.number, F.text)
async def edit_id(message: Message, state: FSMContext) -> None:
    if not message.text.isdigit():
        await message.answer('Вводите только цифры!')
        return
    for item in USER_DATA[message.from_user.id]:
        if item['transaction_number'] == int(message.text):
            await state.update_data(edit_id=item['transaction_number'])
            await message.answer('Транзакция найдена ✅\nВыберите что хотите изменить:\n', reply_markup=edit_history_keyboard())
            return
    await message.answer('Транзакция с таким номером не найдена.')


@router.callback_query(F.data == 'edit_history:amount')
async def edit_amount(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.set_state(StateEditTransaction.new_amount)
    await callback.message.answer('Введите новую сумму:')


@router.message(StateEditTransaction.new_amount, F.text)
async def save_edit_amount(message: Message, state: FSMContext) -> None:
    if not message.text.isdigit():
        await message.answer('Вводите только цифры!')
        return
    data = await state.get_data()
    id = data['edit_id']
    for item in USER_DATA[message.from_user.id]:
        if item['transaction_number'] == id:
            item['amount_money'] = int(message.text)
            await state.set_state(StateEditTransaction.number)
            await message.answer('Сумма успешно изменена✅\nХотите изменить что-то еще?\n', reply_markup=edit_history_keyboard())
            return
    await message.answer('Транзакция с таким номером не найдена.')


@router.callback_query(F.data == 'edit_history:category')
async def edit_category(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.set_state(StateEditTransaction.new_category)
    await callback.message.answer('Выберите новую категорию:', reply_markup=change_history_category_keyboard(callback.from_user.id))


@router.callback_query(StateEditTransaction.new_category)
async def save_edit_category(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    data = await state.get_data()
    id = data['edit_id']
    button_text = get_button_text(callback)
    for item in USER_DATA[callback.from_user.id]:
        if item['transaction_number'] == id:
            item['category'] = button_text
            await state.set_state(StateEditTransaction.number)
            await state.set_state(StateEditTransaction.number)
            await callback.message.answer('Категория успешно изменена✅\nХотите изменить что-то еще?\n',reply_markup=edit_history_keyboard())
            return
    await callback.message.answer('Транзакция с таким номером не найдена.')


@router.callback_query(F.data == 'edit_history:end_edit')
async def end_edit(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await callback.message.answer('Редактирование завершено!✅')
    await state.clear()


@router.message(F.text == 'Информация по доступным командамℹ️')
async def get_info(message: Message) -> None:
    await message.answer('Доступные команды:\n'
                         '/menu - Открыть главное меню\n'
                         '/cancel - Отменить/Прервать действие')


@router.message(F.text == 'Настройки⚙️')
async def choice_settings(message: Message) -> None:
    await message.answer('Список настроек:\n', reply_markup=limits_keyboard())


@router.callback_query(F.data == 'limits:set_limit_month')
async def process_set_limit_for_month(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.set_state(StateSetAmount.amount)
    await callback.message.answer('Установите лимит:')


@router.message(StateSetAmount.amount)
async def set_limit_for_month(message: Message, state: FSMContext) -> None:
    if not message.text.isdigit():
        await message.answer('Вводите только цифры!')
        return
    await state.update_data(amount=message.text)
    set_limit_month(message.from_user.id, 'total_budget', amount=float(message.text))
    await message.answer(f'Лимит на месяц установлен {float(message.text)}')
    await state.clear()


@router.callback_query(F.data == 'limits:set_limit_category')
async def process_set_limit_for_category(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.set_state(StateSetAmountCategory.category)
    await callback.message.answer('Выберите категорию для установки лимита:\n', reply_markup=limits_for_category_keyboard(callback.from_user.id))


@router.callback_query(StateSetAmountCategory.category, F.data.startswith('limits_category:'))
async def process_set_limit_amount(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    key = callback.data.split(':', 1)[1]
    await state.set_state(StateSetAmountCategory.amount)
    await state.update_data(category=key)
    await callback.message.answer('Введите сумму лимита:')


@router.message(StateSetAmountCategory.amount, F.text)
async def set_amount_limit_category(message: Message, state: FSMContext) -> None:
    if not message.text.isdigit():
        await message.answer('Вводите только цифры!')
        return
    await state.update_data(amount=message.text)
    data = await state.get_data()
    user_cats = USER_CATEGORIES[message.from_user.id]
    category_name = user_cats.get(data['category'], data['category'])
    set_limit_category(message.from_user.id, data['category'], float(data['amount']))
    await message.answer(f'Лимит на категорию {category_name} установлен в размере {float(data['amount'])}')
    await state.clear()


@router.callback_query(F.data == 'limits:add_category')
async def process_add_type_cat(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.set_state(StateCreateCategory.type_category)
    await callback.message.answer('Выберите тип транзакции:\n', reply_markup=create_category_type_keyboard())


@router.callback_query(StateCreateCategory.type_category)
async def process_add_name_cat(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    key = callback.data.split(':', 1)[1]
    await state.update_data(type_category=key)
    await state.set_state(StateCreateCategory.name)
    await callback.message.answer('Введите название категории с эмодзи или без как желаете🤗')


@router.message(StateCreateCategory.name, F.text)
async def add_name_category(message: Message, state: FSMContext) -> None:
    name_category = message.text
    user_id = message.from_user.id
    data = await state.get_data()
    type_cat = data.get('type_category')
    if user_id not in USER_CATEGORIES:
        USER_CATEGORIES[user_id] = {}
    count = len(USER_CATEGORIES[user_id])
    USER_CATEGORIES[user_id][f'{type_cat}_{count + 1}'] = name_category
    await message.answer(f'Категория успешно добавлена {name_category}! ✅')
    await state.clear()


@router.callback_query(F.data == 'limits:delete_category')
async def select_del_category(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.answer('Выберите категорию которую хотите удалить.', reply_markup=del_category_keyboard(callback.from_user.id))


@router.callback_query(F.data.startswith('del_cat:'))
async def del_category(callback: CallbackQuery) -> None:
    await callback.answer()
    key = callback.data.split(':', 1)[1]
    name_del_cat = USER_CATEGORIES[callback.from_user.id].pop(key, None)
    await callback.message.answer(f'Категория успешно удаленна: {name_del_cat}')


@router.callback_query(F.data == 'limits:edit_category')
async def select_edit_category(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.answer('Выберите категорию которую хотите редактировать:', reply_markup=edit_category_keyboard(callback.from_user.id))


@router.callback_query(F.data.startswith('edit_cat'))
async def edit_category(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    key = callback.data.split(':', 1)[1]
    await state.update_data(edit_category_key=key)
    await state.set_state(StateEditCategory.name)
    await callback.message.answer('Ведите новое название для категории:')


@router.message(StateEditCategory.name, F.text)
async def save_edit_name(message: Message, state: FSMContext) -> None:
    new_name = message.text
    data = await state.get_data()
    key_category = data.get('edit_category_key')
    USER_CATEGORIES[message.from_user.id][key_category] = new_name
    await message.answer(f'Название категории успешно изменено {new_name}! ✅')
    await state.clear()


@router.message(StateExpensesRevenue.amount_money, F.text)
@router.message(StateCreateCategory.type_category, F.text)
@router.message(StateSetAmountCategory.category, F.text)
@router.message(StateStatistic.statistics, F.text)
@router.message(StateExpensesRevenue.transaction_type, F.text)
@router.message(StateExpensesRevenue.category, F.text)
async def ignore_text_product(message: Message) -> None:
    await message.answer('Пожалуйста, сделай выбор и  нажми на кнопку.')


@router.message(StateFilter(None), F.text)
async def other(message: Message) -> None:
    await message.answer('Нажми /start что бы открыть главное меню.')