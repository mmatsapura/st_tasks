# Демо 3. Агрегация: целое держит уже существующие объекты.
#
# Музыкант жил до группы и будет жить после. Его передают внутрь,
# а не создают в Band.__init__. Одного и того же человека можно
# позвать в две группы — это тот же объект (проверка `is`).
#
# Отличие от композиции не в синтаксисе Python, а в смысле:
#   композиция — "часть принадлежит целому, снаружи её не было";
#   агрегация — "целое ссылается на независимое, его можно шарить".
#
# Если написать Band, который сам делает Musician("Ira") внутри,
# это уже композиция, и Ира не сможет состоять в другой группе
# как тот же объект — получится двойник с тем же именем.


class Musician:
    def __init__(self, name):
        self.name = name

    def play(self):
        return f"{self.name} plays"

    def __str__(self):
        return f"Musician({self.name})"


class Band:
    def __init__(self, name):
        self.name = name
        self.members = []

    def add_member(self, musician):
        # Агрегация: принимаем готового человека, не создаём его здесь.
        self.members.append(musician)


ira = Musician("Ira")
oleg = Musician("Oleg")

lambda_band = Band("Lambda")
recursion = Band("Recursion")

lambda_band.add_member(ira)
lambda_band.add_member(oleg)
recursion.add_member(ira)        # та же Ira, вторая группа

print(ira)                       # Musician(Ira) — существует без группы
print(lambda_band.members[0] is ira)     # True
print(recursion.members[0] is ira)       # True — не копия, тот же объект
print(ira.play())                # Ira plays
