# Демо 2. Классы уже разные — а абстракции всё ещё нет.
#
# Кажется, что проблема прошлого файла решена: квиз, экзамен и проект
# больше не лежат в одном if. У проекта поле tasks, у остальных его нет.
# Это уже лучше (детали разъехались по детям).
#
# Но политику "как считать процент" скопировали трижды.
# Абстракция — не "завести несколько классов", а решить:
#   что РАЗНОЕ (максимум баллов) → остаётся у ребёнка;
#   что ОБЩЕЕ (формула процента, порог сдачи) → одно место, не копия.
#
# Проверка на понимание: если учитель попросит округлять до целых,
# сколько методов придётся править в этом файле? Три. Значит, общее
# решение живёт не там.


class Quiz:
    def __init__(self, title):
        self.title = title

    def max_score(self):
        return 10

    def percent(self, score):
        # Та же формула, что у Exam и Project. Завтра разъедутся.
        return round(score / self.max_score() * 100, 1)


class Exam:
    def __init__(self, title):
        self.title = title

    def max_score(self):
        return 100

    def percent(self, score):
        return round(score / self.max_score() * 100, 1)


class Project:
    def __init__(self, title, tasks):
        self.title = title
        self.tasks = tasks  # лишняя деталь осталась у того, кому она нужна

    def max_score(self):
        return self.tasks * 10

    def percent(self, score):
        return round(score / self.max_score() * 100, 1)


print(Quiz("Week 1").percent(8))            # 80.0
print(Exam("Midterm").percent(80))          # 80.0
print(Project("Coursework", 5).percent(40)) # 80.0
