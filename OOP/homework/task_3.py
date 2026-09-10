# Задание 3. Парковка
#
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
#
# Пример:
#     lot = ParkingLot("Center", 2)
#     toyota = Car("AA1234", "Toyota", CarKind.CAR)
#     honda = Car("BB7777", "Honda", CarKind.MOTO)
#
#     print(toyota)                        # AA1234 Toyota (car)
#     print(len(lot))                      # 0
#     print(bool(lot))                     # False
#
#     lot.park(toyota)
#     print(len(lot))                      # 1
#     print(lot)                           # ParkingLot(Center): 1/2
#     print(lot["AA1234"] is toyota)       # True
#
#     lot.add_from_dict({"plate": "CC0001", "model": "Yamaha", "kind": "moto"})
#     print(len(lot))                      # 2
#
#     left = lot.leave("CC0001")
#     print(left.model)                    # Yamaha
#     print(len(lot))                      # 1
#
#     with ParkingStay(lot, honda):
#         print(len(lot))                  # 2
#     print(len(lot))                      # 1
#
#     try:
#         with ParkingStay(lot, honda):
#             raise RuntimeError("alarm")
#     except RuntimeError:
#         pass
#     print(len(lot))                      # 1
#
#     other = ParkingLot("East", 10)
#     other.park(Car("AA1234", "Toyota", CarKind.CAR))
#     print(lot == other)                  # True
#
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
