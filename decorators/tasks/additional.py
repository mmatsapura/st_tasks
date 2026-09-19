# Task 1
# Напиши декоратор time_it:
# замерить время работы функции, напечатать
# "Function <name> executed in <seconds> seconds"
# и вернуть результат функции.


# @time_it
def slow_operation():
    total = 0
    for i in range(10_000_000):
        total += i
    return total


result = slow_operation()
print("Result:", result)


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


# @cache
def slow_add(a, b):
    print("Computing...")
    return a + b


print(slow_add(2, 3))
print(slow_add(2, 3))
print(slow_add(4, 5))
print(slow_add(2, 3))


# Task 3
# Сейчас все lambda печатают 25. Исправь так, чтобы вывелось:
# 1 4 9 16 25

functions = []

for n in range(1, 6):
    functions.append(lambda: n * n)

for func in functions:
    print(func())
