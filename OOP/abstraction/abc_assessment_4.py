# Демо 4. ABC: контракт обязательный, алгоритм по-прежнему общий.
#
# Полиморфизм уже показывал ABC ("нельзя забыть area / pay").
# Здесь другой акцент: ABC стоит НАД общим алгоритмом, а не вместо него.
#
# Разделение ролей в Assessment:
#   kind(), max_score()  — абстрактные: без них объект не существует;
#   percent(), passed()  — обычные: дети их НЕ пишут и НЕ копируют.
#
# Если percent() тоже пометить @abstractmethod, придётся повторить формулу
# в каждом ребёнке — вернёмся к файлу 2. Абстрактным делают то, что
# РАЗНОЕ, не то, что общее.
#
# Project по-прежнему единственный с tasks. Assessment про задания не знает.
# Это проверка: "лишняя деталь уехала к ребёнку, контракт от этого не раздулся".


from abc import ABC, abstractmethod


class Assessment(ABC):
    def __init__(self, title):
        self.title = title

    @abstractmethod
    def kind(self):
        pass

    @abstractmethod
    def max_score(self):
        pass

    def percent(self, score):
        # Обычный метод: политика одна, максимум спрашиваем у ребёнка.
        return round(score / self.max_score() * 100, 1)

    def passed(self, score):
        return self.percent(score) >= 60


class Quiz(Assessment):
    def kind(self):
        return "quiz"

    def max_score(self):
        return 10


class Exam(Assessment):
    def kind(self):
        return "exam"

    def max_score(self):
        return 100


class Project(Assessment):
    def __init__(self, title, tasks):
        super().__init__(title)
        self.tasks = tasks

    def kind(self):
        return "project"

    def max_score(self):
        return self.tasks * 10


quiz = Quiz("Week 1")
exam = Exam("Midterm")
project = Project("Coursework", 5)

print(quiz.kind())                 # quiz
print(quiz.percent(8))             # 80.0
print(exam.passed(50))             # False
print(project.max_score())         # 50
print(isinstance(project, Assessment))  # True

# Теперь падает на СОЗДАНИИ, не на вызове:
# Assessment("x")                  # TypeError
#
# class Lab(Assessment):
#     pass
#
# Lab("Lab 1")                     # TypeError: нет kind и max_score
