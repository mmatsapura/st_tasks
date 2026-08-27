# Задание 1. Абстракция + наследование + полиморфизм
#
# Сделай иерархию транспорта. Базовый класс задаёт контракт (абстракция),
# дочерние классы реализуют его по-разному (наследование), а общий код
# вызывает одни и те же методы, не зная конкретный тип (полиморфизм).
#
# Требования:
#
# 1. Класс Vehicle(ABC) — абстракция
#    Конструктор: Vehicle(name)
#    - name — публичный атрибут
#    - абстрактный метод kind() — возвращает строку с типом транспорта
#    - абстрактный метод consumption() — расход на 100 км (число)
#    - абстрактный метод move() — возвращает строку, как движется транспорт
#    - сам Vehicle создавать нельзя
#
# 2. Обычный метод trip_cost(km, price) в Vehicle (не абстрактный):
#    - считает стоимость поездки: consumption() / 100 * km * price
#    - округлить до 2 знаков
#    - km должен быть > 0, price должен быть >= 0
#    - иначе TypeError или ValueError
#    - этот метод общий: дети его не дублируют
#
# 3. Класс Car(Vehicle) — наследование
#    Конструктор: Car(name, liters_per_100)
#    - вызвать super().__init__(name)
#    - liters_per_100 — публичный атрибут, положительный int или float
#    - иначе TypeError или ValueError
#    - kind() возвращает "car"
#    - consumption() возвращает liters_per_100
#    - move() возвращает: "{name} drives on the road."
#
# 4. Класс Bike(Vehicle) — второй наследник того же родителя
#    Конструктор: Bike(name)
#    - kind() возвращает "bike"
#    - consumption() возвращает 0
#    - move() возвращает: "{name} rides the lane."
#
# 5. Класс Truck(Car) — многоуровневое наследование
#    Конструктор: Truck(name, liters_per_100, capacity_tons)
#    - вызвать super().__init__(name, liters_per_100)
#    - capacity_tons — публичный атрибут, положительный int или float
#    - иначе TypeError или ValueError
#    - kind() переопределить: возвращает "truck"
#    - move() переопределить: "{name} hauls cargo."
#
# 6. Полиморфизм — две функции:
#    - start_all(vehicles) вызывает move() у каждого и возвращает список строк
#    - total_cost(vehicles, km, price) складывает trip_cost(...) всех
#      элементов и возвращает число (округление не нужно поверх суммы:
#      каждый trip_cost уже округлён до 2 знаков)
#
# 7. __str__:
#    Car("Toyota", 7)       -> Car(Toyota): 7.0 L/100km
#    Bike("Giant")          -> Bike(Giant): 0.0 L/100km
#    Truck("Volvo", 22, 10) -> Truck(Volvo): 22.0 L/100km, 10.0 t
#
# Пример:
#     car = Car("Toyota", 7)
#     bike = Bike("Giant")
#     truck = Truck("Volvo", 22, 10)
#
#     print(car.kind())                     # car
#     print(car.move())                     # Toyota drives on the road.
#     print(car.trip_cost(100, 50))         # 350.0
#     print(bike.trip_cost(100, 50))        # 0.0
#     print(truck.move())                   # Volvo hauls cargo.
#     print(truck.capacity_tons)            # 10
#     print(car)                            # Car(Toyota): 7.0 L/100km
#     print(truck)                          # Truck(Volvo): 22.0 L/100km, 10.0 t
#
#     print(start_all([car, bike, truck]))
#     # ['Toyota drives on the road.',
#     #  'Giant rides the lane.',
#     #  'Volvo hauls cargo.']
#
#     print(total_cost([car, bike, truck], 100, 50))   # 1450.0
#
#     print(isinstance(truck, Car))         # True
#     print(isinstance(truck, Vehicle))     # True
#     print(isinstance(bike, Car))          # False
#
# Некорректные случаи (должны выбрасывать исключение):
#     Vehicle("x")                          # TypeError
#     Car("Toyota", 0)                      # ValueError
#     Truck("Volvo", 22, 0)                 # ValueError
#     car.trip_cost(0, 50)                  # ValueError
#     car.trip_cost(100, -1)                # ValueError
#
#     class Boat(Vehicle):
#         pass
#     Boat()                                # TypeError (нет kind, consumption, move)


# Additional links:
# https://www.geeksforgeeks.org/python/python-oops-concepts/
# https://www.geeksforgeeks.org/python/polymorphism-in-python/
# https://www.geeksforgeeks.org/python/inheritance-in-python/
# https://www.geeksforgeeks.org/python/encapsulation-in-python/
#