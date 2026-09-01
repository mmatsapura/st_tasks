# Демо 2. Композиция: целое создаёт части и владеет ими.
#
# Комната без этого дома в модели не появляется: её не передали с улицы,
# её построили внутри House. Уничтожили дом (в голове, не в GC) — комнаты
# этой планировки больше никому не нужны.
#
# В Python нет unique_ptr. Композицию видно по дизайну:
#   1) часть создаётся внутри целого (в __init__ или в методе);
#   2) снаружи готовый Room в конструктор не просят;
#   3) эту же комнату не кладут во второй дом.
#
# Это не "список строк с названиями". Room — отдельный объект
# со своими данными, но жизнь его привязана к дому.


class Room:
    def __init__(self, name, area):
        self.name = name
        self.area = area

    def __str__(self):
        return f"{self.name} ({self.area} m2)"


class House:
    def __init__(self, address):
        self.address = address
        # Композиция: дом сам строит комнаты. Снаружи их ещё не было.
        self.rooms = [
            Room("kitchen", 12),
            Room("bedroom", 16),
        ]

    def add_room(self, name, area):
        # Снова создаём внутри, а не принимаем готовый Room.
        room = Room(name, area)
        self.rooms.append(room)
        return room

    def area(self):
        return sum(room.area for room in self.rooms)


house = House("Shevchenka 1")
print(house.rooms[0])            # kitchen (12 m2)
print(house.area())              # 28

bath = house.add_room("bath", 5)
print(bath)                      # bath (5 m2)
print(house.area())              # 33

# Сравнить с агрегацией в следующем файле:
# комнату не шарят между двумя домами. Это планировка ЭТОГО дома.
