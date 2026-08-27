# Задание: Инкапсуляция
#
# Создай класс Product, который скрывает цену и скидку за контролируемым API.
# Некорректные значения нужно отклонять. Итоговую цену не храни как поле -
# вычисляй её из приватных данных.
#
# Требования:
# 1. Конструктор: Product(title, price, discount=0)
#    - title — публичный атрибут
#    - price и discount хранятся в приватных атрибутах
#
# 2. Цена — методы getter и setter:
#    - get_price() возвращает каталожную цену
#    - set_price(value) принимает положительный int или float
#    - иначе нужно выбросить TypeError или ValueError
#
# 3. Скидка — свойство (property):
#    - getter / setter для discount
#    - значение должно быть числом от 0 до 100 (включительно)
#    - иначе нужно выбросить TypeError или ValueError
#
# 4. final_price — свойство только для чтения:
#    - формула: price * (1 - discount / 100), округление до 2 знаков
#    - присвоить значение final_price должно быть невозможно
#
# 5. __str__ должен выглядеть так:
#    Python Basics: 400.00 , discount 10%, to pay 360.00
#
# Пример:
#     book = Product("Python Basics", 400, discount=10)
#     print(book.get_price())    # 400.0
#     print(book.discount)       # 10.0
#     print(book.final_price)    # 360.0
#
#     book.set_price(500)
#     book.discount = 25
#     print(book)                # Python Basics: 500.00 , discount 25%, to pay 375.00
#
# Некорректные случаи (должны выбрасывать исключение):
#     book.set_price(0)          # ValueError
#     book.discount = 150        # ValueError
#     book.final_price = 10      # AttributeError

