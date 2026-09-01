# Демо 3. Общий алгоритм наверху, детали внизу — но контракт ещё мягкий.
#
# percent() и passed() написаны один раз. Они зовут max_score() —
# сработает версия ребёнка. Это и есть "обычный метод поверх отличий":
# родитель задаёт политику, ребёнок подставляет число.
#
# Project по-прежнему единственный, кто знает про tasks. Родитель
# это поле не объявляет — абстракция: отбросили то, что не всем нужно.
#
# Слабое место (уже видели в полиморфизме): max_score у родителя
# бросает NotImplementedError. Объект Assessment("x") СОЗДАСТЬСЯ.
# Пустой Lab("Lab 1") тоже. Ошибка придёт позже, на вызове percent().
# Если такой объект уже положили в список оценок — поздно.
#
# Следующий файл закрепит контракт через ABC: нельзя создать,
# пока не реализованы обязательные методы.


class Assessment:
    def __init__(self, title):
        self.title = title

    def max_score(self):
        # Мягкий контракт: "дети обязаны переопределить".
        # Python сам это не проверит в момент Assessment(...) / Lab(...).
        raise NotImplementedError("Subclass must implement max_score().")

    def percent(self, score):
        # Общая политика. Не поле max_points на Assessment, а запрос
        # к ребёнку: "какой у тебя максимум?". Формулу правим здесь один раз.
        return round(score / self.max_score() * 100, 1)

    def passed(self, score):
        # Ещё одна общая политика (порог 60%), тоже не копируется в детях.
        return self.percent(score) >= 60


class Quiz(Assessment):
    def max_score(self):
        return 10


class Exam(Assessment):
    def max_score(self):
        return 100


class Project(Assessment):
    def __init__(self, title, tasks):
        super().__init__(title)
        # Деталь "сколько заданий" живёт только здесь.
        self.tasks = tasks

    def max_score(self):
        return self.tasks * 10


print(Quiz("Week 1").percent(8))            # 80.0
print(Exam("Midterm").passed(80))           # True
print(Project("Coursework", 5).percent(40)) # 80.0

# Раскомментировать на занятии и сравнить с abc_assessment_4.py:
# Assessment("x")                 # объект создался — это проблема
# Assessment("x").percent(10)     # NotImplementedError, уже поздно
#
# class Lab(Assessment):
#     pass
#
# Lab("Lab 1")                    # объект создался, хотя max_score нет
# Lab("Lab 1").percent(5)         # NotImplementedError
