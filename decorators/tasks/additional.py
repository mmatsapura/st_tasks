# Task 1
# Напиши декоратор time_it:
# замерить время работы функции, напечатать
# "Function <name> executed in <seconds> seconds"
# и вернуть результат функции.

import functools
import time


def time_it(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        results = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'"Function {func.__name__} executed in {total_time:.4f} seconds"')
        return results
    return wrapper



@time_it
def slow_operation():
    total = 0
    for i in range(10_000_000):
        total += i
    return total


result = slow_operation()
print("Result:", result)
#_______________________________________________________________________________________
# Task 2
# Напиши декоратор cache.
#
# Нужно запоминать результаты функции в словаре: ключ — аргументы, значение — результат.
# При вызове:
#   - если такой ключ уже есть — вернуть сохранённое значение, функцию НЕ вызывать;
#   - если ключа нет — вызвать функцию, сохранить результат, вернуть его.
#
# Тело slow_add не меняй. "Computing..." печатается только когда функция реально считается.
#
# Разбор вызовов:
#   slow_add(2, 3)  -> нет в кеше, считаем, печатаем Computing..., возвращаем 5
#   slow_add(2, 3)  -> уже в кеше, Computing... нет, возвращаем 5
#   slow_add(4, 5)  -> новая пара, считаем, печатаем Computing..., возвращаем 9
#   slow_add(2, 3)  -> снова из кеша, Computing... нет, возвращаем 5
#
# Ожидаемый вывод:
# Computing...
# 5
# 5
# Computing...
# 9
# 5

def cache(func):
    dict_for_results = {}
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if args not in dict_for_results.keys():
            results = func(*args, **kwargs)
            dict_for_results[args] = results
            return dict_for_results[args]
        else:
            return dict_for_results[args]
    return wrapper

@cache
def slow_add(a, b):
    print("Computing...")
    return a + b


print(slow_add(2, 3))
print(slow_add(2, 3))
print(slow_add(4, 5))
print(slow_add(2, 3))

#_______________________________________________________________________________________
# Task 3
# Сейчас все lambda печатают 25. Исправь так, чтобы вывелось:
# 1 4 9 16 25

functions = []

for n in range(1, 6):
    functions.append(lambda x= n: x * x)

for fun in functions:
    print(fun())
