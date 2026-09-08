# Демо 4. @dataclass
#
# Датакласс сам пишет __init__, __repr__ и __eq__ по полям.
# Это не замена ООП: методы и валидацию всё равно пишешь сам.
# frozen=True — объект нельзя менять после создания.


from dataclasses import dataclass, field


@dataclass
class Point:
    x: float
    y: float


@dataclass(frozen=True)
class Ticket:
    event: str
    price: float
    tags: list = field(default_factory=list)

    def with_tax(self):
        return round(self.price * 1.2, 2)


p1 = Point(1, 2)
p2 = Point(1, 2)
print(p1)                      # Point(x=1, y=2) — __repr__ бесплатно
print(p1 == p2)                # True — __eq__ по полям

ticket = Ticket("PyCon", 100)
print(ticket.with_tax())       # 120.0
# ticket.price = 50            # FrozenInstanceError
