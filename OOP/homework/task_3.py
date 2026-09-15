# Задание 3. Парковка
#_______________________________________________________________________________________
from enum import Enum
from dataclasses import dataclass
from pydantic import BaseModel, Field
from typing import Annotated, Any


class CarKind(Enum):
    CAR = 'car'
    MOTO = 'moto'


class ParkingError(Exception):
    pass


class FullError(ParkingError):
    def __init__(self):
        super().__init__('Мест нет')


class DuplicatePlateError(ParkingError):
    def __init__(self, plate):
        self.plate =plate
        super().__init__(f'Машина с таким номерным знаком: {self.plate} уже стоит в паркинге')


class UnknownPlateError(ParkingError):
    def __init__(self, plate):
        self.plate = plate
        super().__init__(f'Машины с таким номером нет {self.plate}')


@dataclass(frozen=True)
class Car:
    plate: str
    model: str
    kind: CarKind

    def __post_init__(self):
        if not isinstance(self.plate, str) or not isinstance(self.model, str):
            raise TypeError('plate и model должны быть строкой')
        if not self.plate or not self.model:
            raise ValueError('plate и model не могут быть пустыми')

    def __str__(self):
        return f'{self.plate} {self.model} ({self.kind.value})'


class CarIn(BaseModel):
    plate: Annotated[str, Field(min_length=3)]
    model: Annotated[str, Field(min_length=1)]
    kind: CarKind


class ParkingLot:
    def __init__(self, name: str, capacity: int):
        # Увидел в видео, что делал человек так, показалось это разумным решением вынести
        # проверки в отдельный метод, это уместно или лучше в самом init сразу и проверять данные?
        self.verify_name(name)
        self.verify_capacity(capacity)

        self.name = name
        self.capacity = capacity
        self.__data = {}

    @staticmethod
    def verify_name(name: str):
        if not name:
            raise ValueError('name не может быть пустым')
        if not isinstance(name, str):
            raise TypeError('name должен быть строкой')

    @staticmethod
    def verify_capacity(capacity: int):
        if not isinstance(capacity, int):
            raise TypeError('capacity должен быть целым числом')
        if capacity <= 0:
            raise ValueError('capacity должно быть положительным числом и больше нуля')

    def park(self, park_car: Car):
        if park_car.plate in self.__data:
            raise DuplicatePlateError(f'{park_car.plate}')
        if len(self.__data) >= self.capacity:
            raise FullError
        self.__data[park_car.plate] = park_car
        return f'Машина припаркована {park_car}'

    def leave(self, plate):
        if plate not in self.__data:
            raise UnknownPlateError(f'{plate}')
        del_car = self.__data.pop(plate)
        return del_car

    def add_from_dict(self, data: dict):
        valid_data = CarIn(**data)
        car_dict = Car(plate=valid_data.plate, model=valid_data.model, kind=valid_data.kind)
        self.park(car_dict)

    def __len__(self):
        return len(self.__data)

    def __bool__(self):
        return len(self.__data) > 0

    def __getitem__(self, plate):
        if plate in self.__data:
            return self.__data[plate]
        raise UnknownPlateError(f'{plate}')

    def __str__(self):
        return f'ParkingLot({self.name}: {self.capacity - len(self.__data)}/{self.capacity})'

    def __repr__(self):
        return  f'ParkingLot({self.name}, capacity={self.capacity}, parked={len(self.__data)})'

    def __eq__(self, other: Any):
        if not isinstance(other, ParkingLot):
            return NotImplemented
        return self.__data.keys() == other.__data.keys()

class ParkingStay:
    def __init__(self, lot, auto):
        self.lot = lot
        self.car = auto

    def __enter__(self):
        return self.lot.park(self.car)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.car is not None:
            self.lot.leave(self.car.plate)
#_______________________________________________________________________________________
# Пример:
# lot = ParkingLot("Center", 2)
# toyota = Car("AA1234", "Toyota", CarKind.CAR)
# honda = Car("BB7777", "Honda", CarKind.MOTO)
#
# print(toyota)                        # AA1234 Toyota (car)
# print(len(lot))                      # 0
# print(bool(lot))                     # False
#
# lot.park(toyota)
# print(len(lot))                      # 1
# print(lot)                           # ParkingLot(Center): 1/2
# print(lot["AA1234"] is toyota)       # True
#
# lot.add_from_dict({"plate": "CC0001", "model": "Yamaha", "kind": "moto"})
# print(len(lot))                      # 2
#
# left = lot.leave("CC0001")
# print(left.model)                    # Yamaha
# print(len(lot))                      # 1
#
# with ParkingStay(lot, honda):
#     print(len(lot))                  # 2
# print(len(lot))                      # 1
#
# try:
#     with ParkingStay(lot, honda):
#         raise RuntimeError("alarm")
# except RuntimeError:
#     pass
# print(len(lot))                      # 1
#
# other = ParkingLot("East", 10)
# other.park(Car("AA1234", "Toyota", CarKind.CAR))
# print(lot == other)                  # True
#_______________________________________________________________________________________
# Ошибки:
#     ParkingLot("", 2)                    # ValueError
#     ParkingLot("Center", 0)              # ValueError
#     Car("", "Toyota", CarKind.CAR)       # ValueError
#     lot.park(toyota)                     # DuplicatePlateError
#     lot.park(Car("ZZ9", "Kia", CarKind.CAR))
#     lot.park(Car("YY1", "Ford", CarKind.CAR))  # FullError
#     lot["NOPE"]                          # UnknownPlateError
#     lot.leave("NOPE")                    # UnknownPlateError
#     CarIn(plate="AB", model="X", kind="car")  # ValidationError
#_______________________________________________________________________________________
# У парковки мало мест. Машины заезжают и выезжают.
# Номер не должен повторяться. Если места кончились — ошибка.
#
# Машину удобно описать датаклассом: поля сами станут аргументами.
# Пустой номер отсекает __post_init__(смотри pythonic_post_init) — он вызывается сразу после создания.
# Данные с формы (словарь) сначала проверяет pydantic, потом машина
# попадает на стоянку.
#
# Заезд через with: вошли в блок — машина стоит, вышли — она уехала.
# Даже если внутри блока случилась ошибка, машину всё равно убрать.
#
# Нужен пакет: pip install pydantic
#
# 1. Enum CarKind
#    CAR = "car"
#    MOTO = "moto"
#
# 2. Свои ошибки (все наследуют ParkingError):
#    ParkingError
#    FullError            — мест нет
#    DuplicatePlateError  — такой номер уже стоит
#    UnknownPlateError    — такого номера нет
#
# 3. @dataclass(frozen=True) Car
#    поля: plate, model, kind
#    если plate или model пустые — ValueError (пиши проверку в __post_init__)
#    print(car) -> AA1234 Toyota (car)
#
# 4. pydantic-модель CarIn
#    plate — строка, минимум 3 символа
#    model — строка, минимум 1 символ
#    kind — CarKind
#    плохие данные -> ValidationError
#
# 5. Класс ParkingLot(name, capacity)
#    name не пустой, иначе ValueError
#    capacity целое число > 0, иначе TypeError или ValueError
#
#    park(car)   — поставить машину
#                  номер уже есть -> DuplicatePlateError
#                  мест нет -> FullError
#    leave(plate) — убрать машину и вернуть этот Car
#                  номера нет -> UnknownPlateError
#    add_from_dict(data) — data это словарь, проверить через CarIn,
#                          сделать Car и вызвать park
#
#    len(lot)        — сколько машин стоит
#    bool(lot)       — False, если пусто
#    lot["AA1234"]   — машина с этим номером, иначе UnknownPlateError
#    print(lot)      -> ParkingLot(Center): 2/5
#    repr(lot)       -> ParkingLot('Center', capacity=5, parked=2)
#    lot == other    — True, если одинаковые номера машин
#                      (имя парковки не важно)
#
# 6. Класс ParkingStay(lot, car) для with
#    вход в with  -> park(car)
#    выход из with -> leave(car.plate)
#    если внутри with ошибка — машину всё равно убрать, ошибку не прятать
#_______________________________________________________________________________________