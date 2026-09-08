# Демо 5. Enum и свои исключения
#
# Enum — закрытый набор значений. Не строка "paid"/"Paid"/"оплачен",
# а Status.PAID. Сравнивать можно через is.
#
# Свои исключения — отдельные типы ошибок предметной области.
# except OrderError не поймает ValueError от int(), и наоборот.


from enum import Enum, auto


class Status(Enum):
    NEW = auto()
    PAID = auto()
    CANCELED = auto()


class OrderError(Exception):
    pass


class EmptyOrderError(OrderError):
    pass


class AlreadyPaidError(OrderError):
    pass


class Order:
    def __init__(self, items):
        if not items:
            raise EmptyOrderError("корзина пустая")
        self.items = list(items)
        self.status = Status.NEW

    def pay(self):
        if self.status is Status.PAID:
            raise AlreadyPaidError("заказ уже оплачен")
        self.status = Status.PAID


order = Order(["book"])
print(order.status)            # Status.NEW
print(order.status is Status.NEW)

order.pay()
print(order.status is Status.PAID)

try:
    order.pay()
except AlreadyPaidError as error:
    print(error)

try:
    Order([])
except EmptyOrderError as error:
    print(error)
