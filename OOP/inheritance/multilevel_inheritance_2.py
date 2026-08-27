# Multilevel inheritance: a chain A -> B -> C.
# The grandchild gets everything from both the parent and the grandparent.


class Vehicle:
    def __init__(self, brand):
        self.brand = brand

    def move(self):
        return f"{self.brand} is moving."


class Car(Vehicle):
    def __init__(self, brand, doors):
        super().__init__(brand)  # call Vehicle.__init__
        self.doors = doors

    def honk(self):
        return "Beep!"


class ElectricCar(Car):
    def __init__(self, brand, doors, battery_kwh):
        super().__init__(brand, doors)  # call Car.__init__, which calls Vehicle.__init__
        self.battery_kwh = battery_kwh

    def move(self):
        # Override, but still reuse the parent text through super().
        return super().move() + " Silently."


tesla = ElectricCar("Tesla", 4, 75)

print(tesla.move())         # Tesla is moving. Silently.
print(tesla.honk())         # from Car
print(tesla.doors)          # from Car
print(tesla.battery_kwh)    # from ElectricCar
print(ElectricCar.__mro__)  # ElectricCar -> Car -> Vehicle -> object
