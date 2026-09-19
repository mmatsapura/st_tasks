"""
Напиши три декоратора. Тела функций ниже не меняй.

1) require_login
   Если CURRENT_USER["logged_in"] is False — вернуть "Access denied".
   Иначе вызвать функцию и вернуть её результат.

2) call_limit(times)
   Разрешить не больше times вызовов.
   Дальше вернуть "Call limit exceeded".

3) discount(percent)
   Функция возвращает цену. Вернуть цену со скидкой:
   price * (100 - percent) / 100

На checkout повесь @call_limit(times=2) и @require_login.

Ожидаемый вывод:
Access denied
book added to cart
order paid
order paid
Call limit exceeded
180.0
"""

from functools import wraps


CURRENT_USER = {"logged_in": False}


# --- напиши require_login, call_limit, discount здесь ---


# @require_login
def add_to_cart(item):
    return f"{item} added to cart"


# @call_limit(times=2)
# @require_login
def checkout():
    return "order paid"


# @discount(percent=10)
def apply_welcome_bonus():
    return 200


print(add_to_cart("book"))          # Access denied

CURRENT_USER["logged_in"] = True
print(add_to_cart("book"))          # book added to cart

print(checkout())                   # order paid
print(checkout())                   # order paid
print(checkout())                   # Call limit exceeded

print(apply_welcome_bonus())        # 180.0
