# Multiple inheritance: one child, several parents.
# The child combines independent abilities from each parent.
# If two parents define the same method, the left parent wins (see mro.py).


class Writer:
    def write(self):
        return "writes an article"

    def skill(self):
        return "writing"


class Coder:
    def code(self):
        return "writes Python"

    def skill(self):
        return "coding"


class TechWriter(Writer, Coder):
    def publish(self):
        return f"{self.write()} and {self.code()}."


person = TechWriter()

print(person.write())     # from Writer
print(person.code())      # from Coder
print(person.publish())   # uses both parents
print(person.skill())     # "writing" — Writer is listed first, so it wins

print(TechWriter.__mro__)
# TechWriter -> Writer -> Coder -> object

# Swap the order and the same method would come from Coder instead:
# class TechWriter(Coder, Writer):
#     ...
# person.skill() would then return "coding"
