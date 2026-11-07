from aiogram.fsm.state import State, StatesGroup


class StateExpensesRevenue(StatesGroup):
    amount_money = State()
    transaction_type = State()
    category = State()


class StateStatistic(StatesGroup):
    statistics = State()


class StateSetAmount(StatesGroup):
    amount = State()


class StateSetAmountCategory(StatesGroup):
    category = State()
    amount = State()


class StateCreateCategory(StatesGroup):
    type_category = State()
    name = State()


class StateEditCategory(StatesGroup):
    name = State()


class StateDelTransaction(StatesGroup):
    number = State()


class StateEditTransaction(StatesGroup):
    number = State()
    new_amount = State()
    new_category = State()