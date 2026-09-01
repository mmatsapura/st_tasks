# Задание: Абстракция
#
# Сделай абстрактный конвертер единиц и три реализации.
# Общие шаги (проверка, округление, строка результата) живут в родителе.
# Формула перевода — только в детях: у каждого она своя.
#
# Требования:
#
# 1. Класс Converter(ABC)
#    - абстрактный from_unit() — из какой единицы
#    - абстрактный to_unit() — в какую единицу
#    - абстрактный convert(value) — только формула, без печати и округления
#    - создавать Converter нельзя
#    - конструктора у Converter нет
#
# 2. Обычный метод can_convert(value) в Converter:
#    - по умолчанию возвращает True
#    - переопределяет только тот класс, которому нужна проверка значения
#
# 3. Обычный метод describe(value) в Converter:
#    - value — int или float, иначе TypeError
#    - если can_convert(value) это False — ValueError
#    - иначе строка: "{value} {from_unit} = {результат} {to_unit}"
#    - результат: round(convert(value), 2) — округление здесь, не в детях
#    - дети describe() не пишут
#
# 4. __str__ в Converter:
#    ИмяКласса(from -> to)
#    Пример: KmToMiles(km -> mi)
#    Имя класса и единицы брать из кода, не писать строку вручную в каждом ребёнке
#
# 5. Класс KmToMiles(Converter)
#    - from_unit() → "km", to_unit() → "mi"
#    - convert(value) → value * 0.62137
#    - can_convert(value) → True, если value >= 0
#
# 6. Класс CToF(Converter)
#    - from_unit() → "C", to_unit() → "F"
#    - convert(value) → value * 9 / 5 + 32
#    - can_convert не писать: минусовая температура допустима
#
# 7. Класс CurrencyToUah(Converter)
#    Конструктор: CurrencyToUah(currency, rate)
#    - currency — непустая строка, иначе ValueError
#    - rate — положительный int или float, иначе TypeError или ValueError
#    - from_unit() → currency, to_unit() → "UAH"
#    - convert(value) → value * rate
#    - can_convert(value) → True, если value >= 0
#    - currency и rate — публичные атрибуты
#    - эти поля только у CurrencyToUah, не у Converter
#
# 8. Функция describe_all(converters, value)
#    - вызывает describe(value) у каждого элемента
#    - возвращает список строк
#
# Пример:
#     km = KmToMiles()
#     temp = CToF()
#     usd = CurrencyToUah("USD", 41.2)
#
#     print(km.convert(10))                # ~6.2137  (без округления)
#     print(km.describe(10))               # 10 km = 6.21 mi
#     print(temp.describe(0))              # 0 C = 32.0 F
#     print(temp.describe(-10))            # -10 C = 14.0 F
#     print(usd.describe(10))              # 10 USD = 412.0 UAH
#     print(km)                            # KmToMiles(km -> mi)
#     print(usd)                           # CurrencyToUah(USD -> UAH)
#
#     print(describe_all([km, temp, usd], 10))
#     # ['10 km = 6.21 mi', '10 C = 50.0 F', '10 USD = 412.0 UAH']
#
#     print(isinstance(usd, Converter))    # True
#     print(isinstance(temp, CurrencyToUah))  # False
#
# Некорректные случаи (должны выбрасывать исключение):
#     Converter()                          # TypeError
#     KmToMiles().describe(-1)             # ValueError
#     KmToMiles().describe("10")           # TypeError
#     CToF().describe(-10)                 # не ошибка: -10 C = 14.0 F
#     CurrencyToUah("", 41.2)              # ValueError
#     CurrencyToUah("USD", 0)              # ValueError
#     usd.describe(-5)                     # ValueError
#
#     class Empty(Converter):
#         pass
#     Empty()                              # TypeError (нет from_unit, to_unit, convert)
