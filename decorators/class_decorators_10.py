from timer_decorator_7 import timer


@timer
class Player:
    def __init__(self, name, surname, age, ppg):
        self.name = name
        self.surname = surname
        self.age = age
        self.ppg = ppg

    @timer
    def show_player_info(self):
        return f"{self.name} {self.surname} is {self.age} years old and average {self.ppg} ppg."



MJ = Player(name="Michel", surname="Jordan", age=28, ppg=33)

print(MJ.show_player_info())