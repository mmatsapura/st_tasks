# Задание 4. Прокат

from enum import Enum
from dataclasses import dataclass

from types import TracebackType


class RentStatus(Enum):
    FREE = 'free'
    RESERVED = 'reserved'


class RentItemKind(Enum):
    ROLLER_SKATE = 'Roller skate'
    SKATEBOARD = 'Skateboard'
    SCOOTER = 'Scooter'
    BICYCLE = 'Bicycle'


class RentStatusError(Exception):
    pass


class RentStatusReservedError(RentStatusError):
    pass


class RentStatusNotFoundError(RentStatusError):
    pass


@dataclass
class RentItem:
    id: int
    name: str
    price: float|int
    kind: RentItemKind
    status: RentStatus

    def __post_init__(self):
        if not self.id or not self.name or not self.price:
            raise ValueError

    def __str__(self) -> str:
        return f'{self.name} {self.price} {self.kind.value} {self.status.value}'


class Warehouse:
    def __init__(self):
        self.dict_warehouse = {}
        self.dict_rent = {}

    @staticmethod
    def verify_item(item):
        if not item:
            raise ValueError('Атрибут item не может быть пустым ')
        if not isinstance(item, RentItem):
            raise TypeError('Атрибут item должен быть объектом класса RentItem')

    def put_item(self, item: RentItem):
        self.verify_item(item)
        self.dict_warehouse[item.id] = item

    def take_item(self, item:RentItem):
        self.verify_item(item)
        if item.id not in self.dict_warehouse:
            raise RentStatusNotFoundError(f'Невозможно выдать вещь: ID {item.id} не числится среди свободных')
        if item.status != RentStatus.FREE:
            raise RentStatusReservedError(f'Вещь с ID {item.id} уже находится в аренде')
        item.status = RentStatus.RESERVED
        thing = self.dict_warehouse.pop(item.id)
        self.dict_rent[item.id] = thing
        return thing

    def return_item(self, item: RentItem):
        self.verify_item(item)
        if item.id not in self.dict_rent:
            raise RentStatusNotFoundError(f'Невозможно вернуть вещь: ID {item.id} не числится среди выданных')
        if item.status != RentStatus.RESERVED:
            raise RentStatusReservedError(f'Вещь с ID {item.id} сейчас свободна, ее нельзя вернуть')
        item.status = RentStatus.FREE
        thing = self.dict_rent.pop(item.id)
        self.dict_warehouse[item.id] = thing
        return thing

    def __len__(self):
        return len(self.dict_warehouse) + len(self.dict_rent)

    def __str__(self) -> str:
        info = []
        for v in self.dict_warehouse.values():
            info.append(str(v))
        return '\n'.join(info)

    def __repr__(self) -> str:
        return (f'Склад: {self.dict_warehouse}\n'
                f'Аренда: {self.dict_rent}')

    def __eq__(self, value: object, /) -> bool:
        if not isinstance(value, Warehouse):
            raise ValueError('Атрибут warehouse должен быть объектом класса Warehouse')
        my_all_items = self.dict_warehouse | self.dict_rent
        other_all_items = value.dict_warehouse | value.dict_rent
        if my_all_items.keys() == other_all_items.keys():
            return True
        return False

    def __getitem__(self, item):
        all_items = self.dict_warehouse | self.dict_rent
        if item not in all_items:
           raise RentStatusNotFoundError(f'Вещь с ID {item} не найдена на балансе склада')
        return all_items[item]


class Rent:
    def __init__(self, item: RentItem, warehouse: Warehouse):
        Warehouse.verify_item(item)
        if not isinstance(warehouse, Warehouse):
            raise ValueError('Атрибут warehouse должен быть объектом класса Warehouse')
        self.item = item
        self.warehouse = warehouse

    def __enter__(self):
        return self.warehouse.take_item(self.item)

    def __exit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None):
        if exc_type is not None:
            print(f"Внутри была ошибка: {exc_val}")
        self.warehouse.return_item(self.item)


if __name__ == '__main__':
    my_warehouse = Warehouse()
    my_warehouse2 = Warehouse()
    my_warehouse3 = Warehouse()

    print(len(my_warehouse))

    scooter = RentItem(id=1, name="Xiaomi PRO", price=500, kind=RentItemKind.SCOOTER, status=RentStatus.FREE)
    bike = RentItem(id=2, name="Trek", price=1000, kind=RentItemKind.BICYCLE, status=RentStatus.FREE)
    skateboard = RentItem(id=13, name='Ardis', price=100, kind=RentItemKind.SKATEBOARD, status=RentStatus.RESERVED)

    my_warehouse.put_item(scooter)
    my_warehouse.put_item(bike)

    my_warehouse2.put_item(scooter)
    my_warehouse2.put_item(bike)

    my_warehouse3.put_item(scooter)
    my_warehouse3.put_item(skateboard)

    print(my_warehouse)
    print(len(my_warehouse))

    with Rent(scooter, my_warehouse) as rent:
        print(f"Внутри with статус: {rent.status.value}")
    print(f"После with статус: {scooter.status.value}")

    print(my_warehouse == my_warehouse2)
    print(my_warehouse3 == my_warehouse2)

    try:
        with Rent(bike, my_warehouse) as rent:
            1 / 0
    except ZeroDivisionError:
        print('Была ошибка')
    print(f'После ошибки with статус: {bike.status.value}')


    # my_warehouse.take_item(scooter)
    # try:
    #     my_warehouse.take_item(scooter)
    # except RentStatusReservedError as e:
    #     print(f'Поймали ошибку: {type(e).__name__}')


    print(f'Вещь по ID 1: {my_warehouse[1].name}')

#_______________________________________________________________________________________
# Сделай прокат: велосипеды, самокаты или другой инвентарь.
# Имена классов — на выбор. Один файл .py.
#
# В коде должно быть:
#
# 1. Enum со статусами, например свободен / занят.
#    Не строки "free" / "busy" как обычный текст.
#
# 2. Свои классы ошибок:
#    вещь занята, вещи нет, склад пустой и т.п.
#    Не один ValueError на все случаи.
#
# 3. Вещь — @dataclass или pydantic-модель.
#    Пустое имя / нулевая цена / плохой dict — исключение.
#
# 4. Склад:
#    - положить вещь
#    - взять и вернуть
#    - len(склад) — сколько вещей
#    - print(склад) и repr(склад)
#    - склад1 == склад2 по смыслу (например по списку id), не через is
#    - можно склад["id"] — найти вещь по ключу
#
# 5. with:
#    вход — взять вещь
#    выход — вернуть вещь
#    если внутри with ошибка — вещь всё равно вернуть, ошибку показать
#
# Нельзя:
# - взять уже занятую вещь
# - вернуть вещь, которой нет
# - запихнуть всё в один огромный класс
#
# В if __name__ == "__main__" показать:
# - len и print до и после проката
# - with: после блока вещь свободна
# - with с ошибкой внутри: вещь всё равно свободна
# - вторую попытку взять ту же занятую вещь — своё исключение
# - == или склад["id"]
