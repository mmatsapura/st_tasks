'''
Напиши декоратор retry(times), который повторяет выполнение функции
при возникновении исключения.
times — количество попыток.
Если все попытки неудачны, декоратор выбрасывает последнее исключение.'''


from functools import wraps


def retry(times):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for _ in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    print(f'Ошибка {e}')
            raise last_error
        return wrapper
    return decorator


@retry(times=3)
def risky_action():
    import random
    if random.random() < 0.7:
        raise ValueError("Error!")
    return "Success!"

print(risky_action())
