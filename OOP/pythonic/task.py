# Задание: склад коробок
#
# Сделай маленький склад, используя приёмы из этой папки
# (dunder, dataclass или Enum, своё исключение, with).
#
# 1. Enum BoxStatus: EMPTY, PACKED, SHIPPED
#
# 2. Свои ошибки: WarehouseError и наследник BoxNotFoundError
#
# 3. @dataclass Box:
#    - sku: str, title: str
#    - __str__: "sku: title"
#
# 4. Класс Warehouse:
#    - add(box) кладёт коробку со статусом EMPTY
#    - pack(sku) / ship(sku) меняют статус
#    - pack уже упакованной или отсутствующей — исключение
#    - __len__ — сколько коробок
#    - __str__ / __repr__
#
# 5. Контекстный менеджер Packing:
#    with Packing(warehouse, sku) as box:
#        ...
#    на входе pack(sku), на выходе ship(sku)
#    если внутри ошибка — коробка всё равно не "зависает":
#    статус вернуть в EMPTY (логика — твоя, главное __exit__)
#
# Пример:
#     wh = Warehouse("Dock-1")
#     wh.add(Box("A-1", "Cables"))
#     print(len(wh))                       # 1
#     with Packing(wh, "A-1"):
#         print("packing...")
#     print(wh.status("A-1"))              # BoxStatus.SHIPPED
