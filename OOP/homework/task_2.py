# Задание 2. Автосалон

from abc import ABC, abstractmethod
import datetime


class Dealership:

    def __init__(self):
        self.__sales = []
        self.__clients = {}
        self.__employees = {
            1: Employee(
                name='Игорь',
                person_id=1,
                position='Продавец',
                sales_bonus=0
            )
        }
        self.__cars: dict[int, Car] = {
            1: ElectroCar(
                car_id=1,
                name='Tesla Model 3',
                year=2026,
                body='Седан',
                color='Белый',
                price=45000,
                specifications=['Автопилот', 'Полный привод', 'Доводчики дверей'],
                power_reserve=500
            ),
            2: PetrolCar(
                car_id=2,
                name='BMW X3',
                year=2026,
                body='Кроссовер',
                color='Синий',
                price=60000,
                specifications=['Полный привод', 'Кожаный салон', 'Карбоновый обвес'],
                consumption_100km=10.5
            )
        }

    def add_car(self, car: Car):
        self.__cars[car.car_id] = car

    def show_all_cars(self):
        all_cars_dict = self.__cars.copy()
        return all_cars_dict

    def add_client(self, client: Client):
        self.__clients[client.person_id] = client

    def show_all_clients(self):
        all_clients_dict = self.__clients
        return all_clients_dict

    def add_employees(self, employee: Employee):
        self.__employees[employee.person_id] = employee

    def show_all_employees(self):
        all_employees_dict = self.__employees
        return all_employees_dict

    def sell_car(self, client: Client, employee: Employee, car: Car):
        if client.withdraw_money(car.price):
            amount = car.price / 10
            employee.add_sales_bonus(round(amount, 2))
            new_sales = Order(client, employee, car, car.price)
            self.__sales.append(new_sales)
            del self.__cars[car.car_id]
            print(f'Покупка автомобиля {car.name} прошла успешно.\nПоздравляем {client.name}')
        else:
            print(f'Не достаточно средств на счету для покупки автомобиля {car.name}')

    def show_all_sales(self):
        return self.__sales.copy()


class Order:

    def __init__(self, client, employee, car, price):
        self.client = client
        self.employee = employee
        self.car = car
        self.price = price

#_______________________________________________________________________________________
class Person(ABC):

    def __init__(self, name: str, person_id: int):
        if not name:
            raise ValueError('Атрибут name не может быть пустым')
        if not isinstance(name, str):
            raise TypeError('Атрибут name должно быть строкой (str)')
        self.name = name
        if person_id <= 0:
            raise ValueError('Атрибут person_id не может быть равен или меньше нуля')
        if not isinstance(person_id, int):
            raise TypeError('Атрибут person_id должен быть числом (int)')
        self.__person_id = person_id

    @property
    def person_id(self):
        return self.__person_id

    @abstractmethod
    def get_info(self):
        pass


class Client(Person):

    def __init__(self, name: str, person_id: int, balance: int|float):
        super().__init__(name, person_id)
        if balance < 0:
            raise ValueError('Атрибут balance не может быть отрицательным')
        if not isinstance(balance, (int, float)):
            raise TypeError('Атрибут balance должен быть числом (int или float)')
        self.__balance = balance

    @property
    def balance(self):
        return self.__balance

    def withdraw_money(self, amount: int|float):
        if amount > self.__balance:
            return False
        self.__balance -= amount
        return True

    def get_info(self):
        return (f'Name: {self.name}\n'
                f'ID: {self.person_id}\n'
                f'Balance: {self.balance}$')


class Employee(Person):

    def __init__(self, name: str, person_id: int, position: str, sales_bonus: int|float):
        super().__init__(name, person_id)
        if not isinstance(sales_bonus, (int, float)):
            raise TypeError('Атрибут sales_bonus должен быть числом (float или int)')
        if sales_bonus < 0:
            raise ValueError('Атрибут sales_bonus не может быть равен или меньше нулю')
        self.__sales_bonus = sales_bonus
        if not position:
            raise ValueError('Атрибут position не может быть пустым')
        if not isinstance(position, str):
            raise TypeError('Атрибут position должен быть строкой (str)')
        self.position = position


    @property
    def sales_bonus(self):
        return self.__sales_bonus

    def add_sales_bonus(self, amount: int|float):
        self.__sales_bonus += amount
        return self.__sales_bonus

    def get_info(self):
        return (f'Name: {self.name}\n'
                f'ID: {self.person_id}\n'
                f'Position: {self.position}\n'
                f'Balance: {self.sales_bonus}$')

#_______________________________________________________________________________________
class Car(ABC):

    def __init__(self, car_id: int, name: str, year: int, body: str, color: str,
                 price: int|float, specifications: list[str]):
        if car_id <= 0:
            raise ValueError('Атрибут car_id не может быть равен или меньше нуля')
        if not isinstance(car_id, int):
            raise TypeError('Атрибут car_id должен быть числом (int)')
        self.__car_id = car_id
        if not name:
            raise ValueError('Атрибут name не может быть пустым')
        if not isinstance(name, str):
            raise TypeError('Атрибут name должен быть строкой (str)')
        self.name = name
        current_year = datetime.date.today().year
        if not isinstance(year, int):
            raise TypeError('Атрибут year должен быть числом (int)')
        if year < 0 or year > current_year:
            raise ValueError('Атрибут year не может быть меньше нуля или больше текущего года')
        self.year = year
        if not body:
            raise ValueError('Атрибут body не может быть пустым')
        if not isinstance(body, str):
            raise TypeError('Атрибут body должен быть строкой (str)')
        self.body = body
        if not color:
            raise ValueError('Атрибут color не может быть пустым')
        if not isinstance(color, str):
            raise TypeError('Атрибут color должен быть строкой (str)')
        self.color = color
        if price <= 0:
            raise ValueError('Атрибут price не может быть равен или меньше нуля')
        if not isinstance(price, (int, float)):
            raise TypeError('Атрибут price должен быть числом (int или float)')
        self.__price = price
        if not isinstance(specifications, list):
            raise TypeError('Атрибут specifications должен быть списком (list)')
        for item in specifications:
            if not isinstance(item, str):
                raise TypeError('Каждый элемент specifications должен быть строкой (str)')
        if not specifications:
            raise ValueError("Список specifications не может быть пустым.")
        self.specifications = specifications

    @property
    def car_id(self):
        return self.__car_id

    @property
    def price(self):
        return self.__price

    @abstractmethod
    def get_info(self):
        pass


class ElectroCar(Car):

    def __init__(self,car_id: int, name: str, year: int, body: str, color: str,
                 price: int|float, specifications: list[str], power_reserve: int|float):
        super().__init__(car_id, name, year, body, color, price, specifications)
        if power_reserve <= 0:
            raise ValueError('Атрибут power_reserve не может быть равен или меньше нуля')
        if not isinstance(power_reserve, (int, float)):
            raise TypeError('Атрибут power_reverse должен быть числом (int или float)')
        self.power_reserve = power_reserve

    def get_info(self):
        return (f'ID: {self.car_id}\n'
                f'Name: {self.name}\n'
                f'Year: {self.year}\n'
                f'Body: {self.body}\n'
                f'Color: {self.color}\n'
                f'Price: {self.price}$\n'
                f'Specifications: {self.specifications}\n'
                f'Power reserve: {self.power_reserve}Km')


class PetrolCar(Car):

    def __init__(self, car_id: int, name: str, year: int, body: str, color: str,
                 price: int|float, specifications: list[str], consumption_100km: int|float):
        super().__init__(car_id, name, year, body, color, price, specifications)
        if consumption_100km <= 0:
            raise ValueError('Атрибут consumption_100km не может быть равен или меньше нуля')
        if not isinstance(consumption_100km, (int, float)):
            raise TypeError('Атрибут consumption_100km должен быть числом (int или float)')
        self.consumption_100km = consumption_100km

    def get_info(self):
        return (f'ID: {self.car_id}\n'
                f'Name: {self.name}\n'
                f'Year: {self.year}\n'
                f'Body: {self.body}\n'
                f'Color: {self.color}\n'
                f'Price: {self.price}$\n'
                f'Specifications: {self.specifications}\n'
                f'Fuel consumption: L/100km {self.consumption_100km}')



#_______________________________________________________________________________________
if __name__ == '__main__':

    auto_salon = Dealership()

    car1 = ElectroCar(
        car_id=3,
        name='Nissan Leaf',
        year=2025,
        body='Хэтчбек',
        color='Серый',
        price=30_000,
        specifications=['Камера заднего вида'],
        power_reserve=250
    )

    car2 = PetrolCar(
        car_id=9,
        name='Toyota Camry',
        year=2025,
        body='Седан',
        color='Черный',
        price=35_000,
        specifications=['Кожаный салон', 'Подогрев сидений'],
        consumption_100km=8.5
    )

    auto_salon.add_car(car1)
    auto_salon.add_car(car2)

    cars = auto_salon.show_all_cars()

    print('Автопарк:')
    print('________' * 9)
    for auto in cars.values():
        print(auto.get_info())
        print('________' * 9)

#_______________________________________________________________________________________

    client1 = Client(
        name='Джо',
        person_id=13,
        balance=100_000
    )

    client2 = Client(
        name='Микки',
        person_id=2,
        balance=40_000
    )

    auto_salon.add_client(client1)
    auto_salon.add_client(client2)

    clients = auto_salon.show_all_clients()
    print('Клиенты:')
    print('________' * 9)
    for buyer in clients.values():
        print(buyer.get_info())
        print('________' * 9)

    employee1 = Employee(
        name='Екатерина',
        person_id=5,
        position='Администратор',
        sales_bonus=0
    )

    employee2 = Employee(
        name='Данил',
        person_id=88,
        position='Стажер',
        sales_bonus=0
    )

    auto_salon.add_employees(employee1)
    auto_salon.add_employees(employee2)

    employees = auto_salon.show_all_employees()
    print('Работники автосалона:')
    print('________' * 9)
    for worker in employees.values():
        print(worker.get_info())
        print('________' * 9)

#_______________________________________________________________________________________

    auto_salon.sell_car(client2, employee2, car1)

    car_for_sell = cars[1]
    employee_seller = employees[1]
    auto_salon.sell_car(client1, employee_seller, car_for_sell)
    print('________' * 9)

    print('История продаж:')
    sales = auto_salon.show_all_sales()
    for sale in sales:
        print(f'Чек: {sale.client.name} купил {sale.car.name} за {sale.price}$')
        print(f'Продавец: {sale.employee.name}')
        print('________' * 9)

    print('Бонусы продавцов:')
    print(f'{employee2.name}: {employee2.sales_bonus}$')
    print(f'{employee_seller.name}: {employee_seller.sales_bonus}$')
    print('________' * 9)

    print('Остаток машин в автосалоне:')
    remaining_cars = auto_salon.show_all_cars()
    for auto in remaining_cars.values():
        print(f'{auto.name} (ID: {auto.car_id})')

    print('________' * 9)

#_______________________________________________________________________________________

    print('Проверка идентичности объектов:')
    print(f'{sales[0].client is client2}')
    print(f'{sales[0].client is client1}')
    print('________' * 9)

#_______________________________________________________________________________________

    print('Некорректные данные:')
    # error_client = Client(
    #                     name='Станислав',
    #                     person_id=99,
    #                     balance=-500
    # )
    #
    # error_employee = employee2 = Employee(
    #                             name='Данил',
    #                             person_id=88,
    #                             position='',
    #                             sales_bonus=0
    # )
    #
    # error_car = PetrolCar(
    #             car_id=9,
    #             name='Toyota Camry',
    #             year=2055,
    #             body='Седан',
    #             color='Черный',
    #             price=35_000,
    #             specifications=['Кожаный салон', 'Подогрев сидений'],
    #             consumption_100km=8.5
    # )


# Цель
# Спроектировать объектную модель автосалона и реализовать её на Python.
# Набор классов, имена и сигнатуры методов не задаются: их определяет
# архитектура решения. Разные корректные модели допустимы.
#
# Предметная область
# Автосалон продаёт автомобили разных типов, работает с клиентами
# и сотрудниками, оформляет сделки и выполняет обслуживание.
# Один и тот же человек может участвовать в нескольких операциях.
# Часть сущностей связана отношением "является" (is-a), часть —
# отношением "имеет" (has-a).
#
# Требования к модели
#
# 1. Абстракция
#    Есть базовый контракт с обязательными методами. Экземпляр
#    абстрактного типа создать нельзя.
#
# 2. Наследование
#    Общее поведение находится в родителе, различное — в потомках.
#    Общий алгоритм не дублируется в каждом наследнике.
#
# 3. Полиморфизм
#    Общий код вызывает одно и то же имя метода у разных типов.
#    Ветвление по isinstance / type для выбора поведения не используется.
#
# 4. Инкапсуляция
#    Критичные данные (цена, идентификаторы, деньги и т.п.) защищены
#    от некорректной записи снаружи. Невалидные значения вызывают
#    исключение.
#
# 5. Композиция
#    Есть целое, которое само создаёт свои части. Без этого целого
#    такие части не существуют.
#
# 6. Агрегация
#    Есть целое, которое хранит уже существующие объекты. Один и тот же
#    объект может входить в несколько связей (тот же экземпляр, не копия
#    с тем же именем).
#
# Ограничения
# - Отношение has-a не заменяется наследованием.
# - Один класс не концентрирует всю логику предметной области.
# - Некорректные данные приводят к исключению (TypeError или ValueError).
#
# Демонстрация
# В блоке if __name__ == "__main__" выполняется сценарий, из которого
# видно работу модели, а не только создание пустых объектов:
# - минимум два разных типа автомобилей обрабатываются одинаковым кодом;
# - объект человека существует независимо и участвует более одного раза
#   (сравнение через is);
# - часть данных появляется только вместе со сделкой, заказом или визитом;
# - попытка записать некорректное значение вызывает исключение.
#
# Оформление
# Решение — один файл .py.
