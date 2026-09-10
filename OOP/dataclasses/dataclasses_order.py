from dataclasses import dataclass

@dataclass(order=True)
class Point:
    name: str
    x: float
    y: float
    x: int
    y: int

p1 = Point("point", 2, 2)
p2 = Point("point1", 2, 2)

print(p1 < p2)  # True, сравнение по полям по порядку
