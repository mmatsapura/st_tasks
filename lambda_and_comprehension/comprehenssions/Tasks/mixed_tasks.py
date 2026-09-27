# Task 1
# Класс Product и Warehouse.
#
# Методы Warehouse (без обычных for, только comprehension / generator):
#   titles()       list comprehension: названия товаров
#   price_map()    dict comprehension: {name: price}
#   categories()   set comprehension: уникальные категории
#   cheap(limit)   generator: yield Product, у которых price < limit
#
# Декоратор @non_empty:
#   если self.products пустой — вернуть "Warehouse is empty",
#   иначе вызвать метод. Повесь на titles.
#
# Ожидаемый вывод:
# ['apple', 'milk', 'bread']
# {'apple': 12, 'milk': 8, 'bread': 5}
# {'food', 'drink'}
# milk 8
# bread 5
# Warehouse is empty
#_______________________________________________________________________________________
from functools import wraps


class Product:
    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category


def non_empty(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.products:
            return 'Warehouse is empty'
        return func(self, *args, **kwargs)
    return wrapper


class Warehouse:
    def __init__(self, products):
        self.products = products

    @non_empty
    def titles(self):
        return [subject.name for subject in self.products]

    def price_map(self):
        return {subject.name: subject.price for subject in self.products}

    def categories(self):
        return {subject.category for subject in self.products}

    def cheap(self, limit):
        return (subject for subject in self.products if subject.price < limit)


stock = Warehouse([
    Product("apple", 12, "food"),
    Product("milk", 8, "drink"),
    Product("bread", 5, "food"),
])

print(stock.titles())
print(stock.price_map())
print(stock.categories())
for item in stock.cheap(10):
    print(item.name, item.price)

print(Warehouse([]).titles())

#_______________________________________________________________________________________
# Task 2
# Класс User(name, scores).
#
#   passed() — True, если есть хотя бы одна оценка >= 10
#
# Функция report(users):
#   list comprehension: имена тех, у кого passed() is True
#   dict comprehension: {name: max(scores)} для всех users
#   вернуть кортеж (имена, словарь)
#
# Декоратор @uppercase_names:
#   берёт результат report — (list, dict),
#   возвращает имена в верхнем регистре, словарь не трогает.
#   Повесь на report.
#
# Ожидаемый вывод:
# ['ANN', 'KATE']
# {'Ann': 12, 'Bob': 8, 'Kate': 10}
#_______________________________________________________________________________________
class User:
    def __init__(self, name, scores):
        self.name = name
        self.scores = scores

    def passed(self):
        return any((score >= 10 for score in self.scores))

def uppercase_names(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        upper_names = [name.upper() for name in result[0]]
        return upper_names, result[1]
    return wrapper


@uppercase_names
def report(users):
    true_name = [user.name for user in users if user.passed()]
    dict_name = {user.name: max(user.scores) for user in users}
    return true_name, dict_name

users = [
    User("Ann", [7, 12, 9]),
    User("Bob", [4, 8]),
    User("Kate", [10, 6, 10]),
]

names, best = report(users)
print(names)
print(best)
#_______________________________________________________________________________________