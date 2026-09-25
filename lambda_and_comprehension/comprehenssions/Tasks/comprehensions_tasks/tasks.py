# Только comprehension или generator. Обычный for в решении не используй.


# Task 1. List comprehension — фильтр
# Оставь только положительные числа.
nums = [3, -1, 0, 7, -5, -10, 12]

result1 = [number for number in nums if number > 0]
print(result1)
# expected: [3, 7, 12]

#_______________________________________________________________________________________
# Task 2. List comprehension — преобразование
# Замени отрицательные числа на квадрат числа, остальные оставь как есть.
nums = [3, -1, 0, 7, -5, -10, 12]

result2 = [number if number > 0 else number * number for number in nums]
print(result2) #[3, 1, 0, 7, 25, 100, 12]
# expected: [3, 0, 0, 7, 0, 0, 12] ?

#_______________________________________________________________________________________
# Task 3. List comprehension — фильтр словарей
# Имена пользователей старше 18.
users = [
    {"name": "Anna", "age": 22},
    {"name": "Oleg", "age": 17},
    {"name": "Ivan", "age": 30},
    {"name": "Olga", "age": 19},
]

result3 = [user['name'] for user in users if user['age'] > 18]
print(result3)
# expected: ['Anna', 'Ivan', 'Olga']

#_______________________________________________________________________________________
# Task 4. List comprehension — вложенный список
# Собери все оценки > 10 в один список.
grades = {
    "Ann": [7, 10, 12],
    "Bob": [12, 5, 11],
    "Kate": [8, 10, 10],
}

result4 = [point for points in grades.values() for point in points if point > 10]
print(result4)
# expected: [12, 12, 11]

#_______________________________________________________________________________________
# Task 5. Dict comprehension
# Словарь {имя: возраст} только для age >= 18.
users = [
    {"name": "Anna", "age": 22},
    {"name": "Oleg", "age": 17},
    {"name": "Ivan", "age": 30},
]

result5 = {user['name']: user['age'] for user in users if user['age'] > 18}
print(result5)
# expected: {'Anna': 22, 'Ivan': 30}

#_______________________________________________________________________________________
# Task 6. Dict comprehension
# {слово: длина} для всех слов.
words = ["apple", "hi", "banana", "ok"]

result6 = {word: len(word) for word in words}
print(result6)
# expected: {'apple': 5, 'hi': 2, 'banana': 6, 'ok': 2}

#_______________________________________________________________________________________
# Task 7. Set comprehension
# Уникальные категории в нижнем регистре.
categories = ["Food", "drink", "FOOD", "Snack", "Drink"]

result7 = {cat.lower() for cat in categories}
print(result7)
# expected: {'food', 'drink', 'snack'}

#_______________________________________________________________________________________
# Task 8. Set comprehension — вложенный список
# Уникальные оценки >= 10.
marks = [
    [5, 12, 11],
    [7, 10, 12],
    [9, 10, 8],
]

result8 = {grade for grades in marks for grade in grades if grade >= 10}
print(result8)
# expected: {10, 11, 12}

#_______________________________________________________________________________________
# Task 9. Generator expression
# Создай генератор квадратов чётных чисел из nums.
# Выведи список значений.
nums = [1, 2, 3, 4, 5, 6]

result9 = (number ** 2 for number in nums if number % 2 == 0)
print(list(result9))

# expected: [4, 16, 36]

#_______________________________________________________________________________________
# Task 10. Generator function
# Напиши функцию errors(lines), которая yield только строки с "ERROR".
lines = [
    "INFO started",
    "ERROR disk full",
    "INFO ok",
    "ERROR timeout",
]

def errors():
    for l in lines:
        if l.startswith('ERROR'):
            yield l

result10 = errors()
print(next(result10))
print(next(result10))
# expected:
# ERROR disk full
# ERROR timeout

#_______________________________________________________________________________________
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

result11 = {user['user']: sum(int(order['total'])
                              for order in orders
                              if order['user'] == user['user']
                              and order['paid'] == True)
                              for user in orders
                              if user['paid'] == True}
print(result11)


# expected: {'Ann': 200, 'Kate': 15}

#_______________________________________________________________________________________
# Task 12. List comprehension — координаты
# Список кортежей (row, col, value) для всех value > 10.
matrix = [
    [1, 15, 2],
    [5, 30, 9],
    [12, 3, 99],
]

result12 = [(row_index, col_index, value)
            for row_index, row_list in enumerate(matrix)
            for col_index ,value in enumerate(row_list) if value > 10]
print(result12)
# expected: [(0, 1, 15), (1, 1, 30), (2, 0, 12), (2, 2, 99)]

#_______________________________________________________________________________________
# Task 13. Set comprehension
# Теги, которые встречаются хотя бы в двух статьях.
articles = [
    {"title": "a", "tags": ["python", "oop"]},
    {"title": "b", "tags": ["python", "sql"]},
    {"title": "c", "tags": ["git", "sql", "python"]},
]

result13 = {tag for artc in articles for tag in artc['tags']
            if sum(tag in a['tags'] for a in articles) >= 2}
print(result13)
# expected: {'python', 'sql'}

#_______________________________________________________________________________________
# Task 14. Dict comprehension со списками в значениях
# Из "LEVEL:message" собери {level: [messages, ...]}.
logs = [
    "ERROR:disk full",
    "INFO:started",
    "ERROR:timeout",
    "INFO:ok",
    "WARNING:slow",
]

result14 = {log.split(':')[0]: [item.split(':')[1] for item in logs
                                if item.startswith(log.split(':')[0])] for log in logs}
print(result14)
# expected:
# {
#     'ERROR': ['disk full', 'timeout'],
#     'INFO': ['started', 'ok'],
#     'WARNING': ['slow'],
# }

#_______________________________________________________________________________________
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

def out_of_stock(value):
    for name, items in value.items():
        for item in items:
            if item['qty'] == 0:
                yield name, item['name']


gen_stock = out_of_stock(shops)
print(next(gen_stock))
print(next(gen_stock))
# expected:
# ('center', 'apple')
# ('west', 'bread')
#_______________________________________________________________________________________