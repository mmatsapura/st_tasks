from dataclasses import dataclass, field

# @dataclass
# class Person:
#     name: str
#     age: int = field(default=18)
#
# p = Person("Alice")
# print(p)
#
#
# @dataclass
# class Team:
#     members: list = field(default_factory=list)
#
# team = Team()
# team.members.append("Alice")
# print(team)


# @dataclass
# class Counter:
#     count: int = field(default=0, init=False)
#
# c = Counter()
# print(c.count)


# @dataclass
# class Example:
#     x: int
#     y: int = field(default=0, repr=False)

#
# @dataclass
# class Example1:
#     x: int
#     y: int = field(default=0, compare=False)
# #

# @dataclass
# class Example2:
#     x: int = field(default=0, metadata={"unit": "meters"})


# dataclass implement __init__, __repr__, __eq__ methods