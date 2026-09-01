# Демо 1. Антипример: "абстракции" нет, есть один толстый класс.
#
# Идея абстракции: родитель знает ЧТО умеем (есть максимум баллов,
# можно посчитать процент), и не знает КАК устроен каждый вид работы.
# Квизу не нужны задания, проекту не нужна шкала "из 100".
#
# Здесь наоборот: один Assessment хранит поля сразу для всех видов
# и выбирает формулу через if/elif по строке kind.
# Смотри, что ломается:
#   1) у квиза появляется поле tasks=None — мусор, который квизу не принадлежит;
#   2) новый вид (лабораторная) = править ЭТОТ класс: новое поле + новая ветка;
#   3) опечатка в kind всплывает только в рантайме, объект при этом создался.
#
# Вывод, который нужно произнести вслух: лишние детали на родителе —
# это не "универсальность", это свалка.


class Assessment:
    def __init__(self, title, kind, tasks=None):
        self.title = title
        self.kind = kind
        # tasks имеет смысл только для проекта. Квиз и экзамен всё равно
        # получают это поле — родитель не смог "не знать" про задания.
        self.tasks = tasks

    def max_score(self):
        # Родитель перечисляет всех детей внутри себя. Это отказ от абстракции:
        # он должен меняться каждый раз, когда появляется новый вид работы.
        if self.kind == "quiz":
            return 10
        if self.kind == "exam":
            return 100
        if self.kind == "project":
            return self.tasks * 10
        raise ValueError("unknown kind")

    def percent(self, score):
        return round(score / self.max_score() * 100, 1)


quiz = Assessment("Week 1", "quiz")
exam = Assessment("Midterm", "exam")
project = Assessment("Coursework", "project", tasks=5)

print(quiz.max_score())          # 10
print(exam.percent(80))          # 80.0
print(project.percent(40))       # 80.0

# Поле, которого у квиза быть не должно:
print(quiz.tasks)                # None
