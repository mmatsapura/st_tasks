# Задание: Инкапсуляция + наследование
#
# Сделай иерархию сотрудников. Базовый класс прячет данные,
# а дочерние классы меняют зарплату только через protected API.
# Приватный пароль в наследниках использовать нельзя.
#
# Требования:
#
# 1. Класс Employee(name, salary, password)
#    - name — публичный атрибут
#    - зарплата хранится в protected-атрибуте _salary
#    - пароль хранится в private-атрибуте __password (публичного getter нет)
#    - бонус хранится в private-атрибуте
#
# 2. Зарплата — методы getter и setter:
#    - get_salary() возвращает зарплату
#    - set_salary(value) принимает положительный int или float
#    - иначе нужно выбросить TypeError или ValueError
#
# 3. bonus — свойство (property):
#    - число от 0 до 50 (включительно)
#    - иначе TypeError или ValueError
#
# 4. income — свойство только для чтения:
#    - формула: salary * (1 + bonus / 100), округление до 2 знаков
#    - присвоить значение income должно быть невозможно
#
# 5. Protected-метод _raise(amount):
#    - увеличивает _salary на положительное число
#    - иначе ValueError
#    - этот метод как раз для дочерних классов
#
# 6. work() возвращает: "{name} works"
#    __str__ выглядит так:
#    Oleg: salary 3000.00, bonus 10%, income 3300.00
#
# 7. Класс Developer(Employee) — одиночное / иерархическое наследование
#    Конструктор: Developer(name, salary, password, language)
#    - вызвать super().__init__(...)
#    - language — публичный атрибут
#    - work() переопределить: "{name} writes {language} code."
#    - promote(amount) вызывает _raise(amount)
#
# 8. Класс Manager(Employee) — второй наследник того же родителя
#    Конструктор: Manager(name, salary, password, team_size)
#    - team_size — публичный атрибут
#    - work() переопределить: "{name} leads a team of {team_size}."
#    - give_raise(amount) вызывает _raise(amount)
#
# 9. Класс TeamLead(Manager) — многоуровневое наследование
#    - cut(amount) уменьшает _salary
#    - amount должен быть положительным, зарплата после cut должна остаться > 0
#    - иначе ValueError
#
# Пример:
#     dev = Developer("Oleg", 3000, "secret", "Python")
#     print(dev.get_salary())           # 3000.0
#     print(dev.bonus)                  # 0.0
#     print(dev.work())                 # Oleg writes Python code.
#
#     dev.bonus = 10
#     dev.promote(500)
#     print(dev.get_salary())           # 3500.0
#     print(dev.income)                 # 3850.0
#     print(dev)                        # Oleg: salary 3500.00, bonus 10%, income 3850.00
#
#     boss = Manager("Anna", 5000, "qwerty", 8)
#     print(boss.work())                # Anna leads a team of 8.
#     boss.give_raise(500)
#     print(boss.get_salary())          # 5500.0
#
#     lead = TeamLead("Ira", 6000, "admin", 3)
#     lead.cut(200)
#     print(lead.get_salary())          # 5800.0
#     print(isinstance(dev, Employee))  # True
#     print(isinstance(boss, Developer))# False
#
# Некорректные случаи (должны выбрасывать исключение):
#     dev.set_salary(0)                 # ValueError
#     dev.bonus = 80                    # ValueError
#     dev.income = 10                   # AttributeError
#     lead.cut(10000)                   # ValueError
#
