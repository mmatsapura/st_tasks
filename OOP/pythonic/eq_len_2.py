# Демо 2. __eq__ и __len__
#
# == без __eq__ сравнивает id: два Money(10) с одинаковыми полями
# всё равно "не равны". __eq__ задаёт равенство по смыслу.
# __len__ включает объект в len() и в bool() (пустой = False).


class Money:
    def __init__(self, amount, currency):
        self.amount = amount
        self.currency = currency

    def __eq__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        return self.amount == other.amount and self.currency == other.currency

    def __repr__(self):
        return f"Money({self.amount}, {self.currency!r})"


class Cart:
    def __init__(self, items):
        self.items = list(items)

    def __len__(self):
        return len(self.items)

    def __repr__(self):
        return f"Cart({self.items!r})"


a = Money(10, "UAH")
b = Money(10, "UAH")
print(a == b)                  # True  (без __eq__ было бы False)
print(a is b)                  # False — это два разных объекта

cart = Cart(["book", "pen"])
print(len(cart))               # 2
print(bool(Cart([])))          # False — пустая корзина
print(bool(cart))              # True
