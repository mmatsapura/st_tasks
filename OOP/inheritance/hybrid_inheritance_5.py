# Hybrid inheritance: mix of hierarchical + multiple inheritance.
# Two branches share a common ancestor, then join again in one child
# (a diamond). Python merges this through MRO, so Person is used once.


class Person:
    def __init__(self, name):
        self.name = name

    def intro(self):
        return f"I am {self.name}."


class Employee(Person):
    def work(self):
        return "works at a company"


class Student(Person):
    def study(self):
        return "studies at university"


class WorkingStudent(Employee, Student):
    def daily_plan(self):
        return f"{self.intro()} {self.study()} and {self.work()}."


intern = WorkingStudent("Ira")

print(intern.intro())       # from Person (shared ancestor)
print(intern.work())        # from Employee
print(intern.study())       # from Student
print(intern.daily_plan())

print(WorkingStudent.__mro__)
# WorkingStudent -> Employee -> Student -> Person -> object
#
# Person appears only once. That is the diamond, resolved by C3 MRO.
# Details are in mro.py.
