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


class Product:
    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category


# def non_empty(...):
#     ...


class Warehouse:
    def __init__(self, products):
        self.products = products

    def titles(self):
        ...

    def price_map(self):
        ...

    def categories(self):
        ...

    def cheap(self, limit):
        ...


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


class User:
    def __init__(self, name, scores):
        self.name = name
        self.scores = scores

    def passed(self):
        ...


# def uppercase_names(...):
#     ...


def report(users):
    ...


users = [
    User("Ann", [7, 12, 9]),
    User("Bob", [4, 8]),
    User("Kate", [10, 6, 10]),
]

names, best = report(users)
print(names)
print(best)
