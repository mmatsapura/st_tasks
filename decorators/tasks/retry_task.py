'''
Напиши декоратор retry(times), который повторяет выполнение функции при возникновении исключения.
times — количество попыток.
Если все попытки неудачны, декоратор выбрасывает последнее исключение.'''


# @retry(times=3)
def risky_action():
    import random
    if random.random() < 0.7:
        raise ValueError("Error!")
    return "Success!"

print(risky_action())
