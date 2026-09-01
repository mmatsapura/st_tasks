# Демо 1. Антипаттерн: is-a там, где нужен has-a.
#
# Наследование отвечает на вопрос "является ли?". Машина является
# транспортом — ок. Машина является двигателем — нет. У двигателя
# свои детали (свечи, лошадиные силы), у машины — другие (кузов, марка).
#
# Если написать class Car(Engine), Python честно ответит:
# isinstance(car, Engine) is True. Это уже ложь в модели:
# завести можно мотор, а не "машину-как-двигатель".
#
# Композиция и агрегация отвечают на другой вопрос: "есть ли у?".
# У машины ЕСТЬ двигатель. Это has-a, не is-a.
# Как именно "есть" — следующий файлы: создать внутри или принять готовый.


class Engine:
    def __init__(self, horsepower):
        self.horsepower = horsepower

    def start(self):
        return f"engine {self.horsepower} hp starts"


class Car(Engine):
    def __init__(self, brand, horsepower):
        super().__init__(horsepower)
        self.brand = brand


car = Car("Toyota", 150)
print(car.start())
print(isinstance(car, Engine))   # True — модель врёт: машина "является" мотором
print(car.horsepower)            # поле мотора торчит прямо на машине

# Правильное направление (развернём в следующих файлах):
# class Car:
#     def __init__(self, brand, engine):
#         self.brand = brand
#         self.engine = engine      # has-a: двигатель — часть или деталь, не родитель
