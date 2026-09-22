"""
Напиши декоратор retry(times), который повторяет выполнение функции
при возникновении исключения.times — количество попыток.
Если все попытки неудачны, декоратор выбрасывает последнее исключение."""


from functools import wraps


def retry(times):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == times -1:
                        raise
            return None
        return wrapper
    return decorator


@retry(times=3)
def risky_action():
    import random
    if random.random() < 0.7:
        raise ValueError("Error!")
    return "Success!"

print(risky_action())
