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

CURRENT_USER = {"logged_in": False}

# --- напиши require_login, call_limit, discount здесь ---

from functools import wraps


def require_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if False in CURRENT_USER.values():
            return 'Access denied'
        return func(*args, **kwargs)
    return wrapper


def call_limit(func = None, times: int = 0):
    def decorator(f):
        count_times = 0
        @wraps(f)
        def wrapper(*args, **kwargs):
            nonlocal count_times
            if count_times >= times:
                return 'Call limit exceeded'
            count_times += 1
            return f(*args, **kwargs)
        return wrapper
    if func is None:
        return decorator
    return decorator(func)


def discount(func = None, percent: int = 0):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            results = f(*args, **kwargs)
            return results * (100 - percent) / 100
        return wrapper
    if func is None:
        return decorator
    return decorator(func)


@require_login
def add_to_cart(item):
    return f"{item} added to cart"


@call_limit(times=2)
@require_login
def checkout():
    return "order paid"


@discount(percent=10)
def apply_welcome_bonus():
    return 200


print(add_to_cart("book"))          # Access denied

CURRENT_USER["logged_in"] = True
print(add_to_cart("book"))          # book added to cart

print(checkout())                   # order paid
print(checkout())                   # order paid
print(checkout())                   # Call limit exceeded

print(apply_welcome_bonus())        # 180.0
