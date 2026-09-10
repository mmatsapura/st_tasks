from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int

p1 = Point(10, 20)
p2 = Point(10, 20)

print(p1)
print(p1 == p2)
