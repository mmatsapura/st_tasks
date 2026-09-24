# Только comprehension или generator. Обычный for в решении не используй.


# Task 1. List comprehension — фильтр
# Оставь только положительные числа.
nums = [3, -1, 0, 7, -5, -10, 12]
# expected: [3, 7, 12]


# Task 2. List comprehension — преобразование
# Замени отрицательные числа на квадрат числа, остальные оставь как есть.
nums = [3, -1, 0, 7, -5, -10, 12]
# expected: [3, 0, 0, 7, 0, 0, 12]


# Task 3. List comprehension — фильтр словарей
# Имена пользователей старше 18.
users = [
    {"name": "Anna", "age": 22},
    {"name": "Oleg", "age": 17},
    {"name": "Ivan", "age": 30},
    {"name": "Olga", "age": 19},
]
# expected: ['Anna', 'Ivan', 'Olga']


# Task 4. List comprehension — вложенный список
# Собери все оценки > 10 в один список.
grades = {
    "Ann": [7, 10, 12],
    "Bob": [12, 5, 11],
    "Kate": [8, 10, 10],
}
# expected: [12, 12, 11]


# Task 5. Dict comprehension
# Словарь {имя: возраст} только для age >= 18.
users = [
    {"name": "Anna", "age": 22},
    {"name": "Oleg", "age": 17},
    {"name": "Ivan", "age": 30},
]
# expected: {'Anna': 22, 'Ivan': 30}


# Task 6. Dict comprehension
# {слово: длина} для всех слов.
words = ["apple", "hi", "banana", "ok"]
# expected: {'apple': 5, 'hi': 2, 'banana': 6, 'ok': 2}


# Task 7. Set comprehension
# Уникальные категории в нижнем регистре.
categories = ["Food", "drink", "FOOD", "Snack", "Drink"]
# expected: {'food', 'drink', 'snack'}


# Task 8. Set comprehension — вложенный список
# Уникальные оценки >= 10.
marks = [
    [5, 12, 11],
    [7, 10, 12],
    [9, 10, 8],
]
# expected: {10, 11, 12}


# Task 9. Generator expression
# Создай генератор квадратов чётных чисел из nums.
# Выведи список значений.
nums = [1, 2, 3, 4, 5, 6]
# expected: [4, 16, 36]


# Task 10. Generator function
# Напиши функцию errors(lines), которая yield только строки с "ERROR".
lines = [
    "INFO started",
    "ERROR disk full",
    "INFO ok",
    "ERROR timeout",
]
# expected:
# ERROR disk full
# ERROR timeout


# Task 11. Dict comprehension + generator внутри
# {user: сумма total} только по заказам с paid=True.
# Пользователей без оплаченных заказов не включай.
orders = [
    {"user": "Ann", "total": 120, "paid": True},
    {"user": "Bob", "total": 40, "paid": False},
    {"user": "Ann", "total": 80, "paid": True},
    {"user": "Kate", "total": 15, "paid": True},
    {"user": "Bob", "total": 10, "paid": False},
]
# expected: {'Ann': 200, 'Kate': 15}


# Task 12. List comprehension — координаты
# Список кортежей (row, col, value) для всех value > 10.
matrix = [
    [1, 15, 2],
    [5, 30, 9],
    [12, 3, 99],
]
# expected: [(0, 1, 15), (1, 1, 30), (2, 0, 12), (2, 2, 99)]


# Task 13. Set comprehension
# Теги, которые встречаются хотя бы в двух статьях.
articles = [
    {"title": "a", "tags": ["python", "oop"]},
    {"title": "b", "tags": ["python", "sql"]},
    {"title": "c", "tags": ["git", "sql", "python"]},
]
# expected: {'python', 'sql'}


# Task 14. Dict comprehension со списками в значениях
# Из "LEVEL:message" собери {level: [messages, ...]}.
logs = [
    "ERROR:disk full",
    "INFO:started",
    "ERROR:timeout",
    "INFO:ok",
    "WARNING:slow",
]
# expected:
# {
#     'ERROR': ['disk full', 'timeout'],
#     'INFO': ['started', 'ok'],
#     'WARNING': ['slow'],
# }


# Task 15. Generator function
# Напиши out_of_stock(shops): yield кортеж (магазин, товар)
# для продуктов с qty == 0.
shops = {
    "center": [
        {"name": "apple", "qty": 0},
        {"name": "milk", "qty": 3},
    ],
    "west": [
        {"name": "bread", "qty": 0},
        {"name": "milk", "qty": 1},
    ],
}
# expected:
# ('center', 'apple')
# ('west', 'bread')
