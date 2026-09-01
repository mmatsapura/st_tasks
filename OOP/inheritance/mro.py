# MRO (Method Resolution Order) is the path Python follows to find a method.
# It uses C3 linearization: left-to-right, children before parents,
# and each class appears only once (this is how the diamond is solved).
#
# Look it up with Class.__mro__ or Class.mro().
# super() does not mean "the parent class" — it means "the next class in MRO".


class A:
    def ping(self):
        print("A.ping")

class Y:
    def ping(self):
        print("Y.ping")


class B(Y):
    def ping(self):
        print("B.ping")
        super().ping()


class C(A):
    def ping(self):
        print("C.ping")
        super().ping()


class D(B, C):
    def ping(self):
        print("D.ping")
        super().ping()


print("MRO of D:", D.mro())
# D -> B -> C -> A -> object
#
#      A
#     / \
#    B   C
#     \ /
#      D

print("--- D().ping() ---")
D().ping()
# D.ping
# B.ping
# C.ping   <- C is next after B in MRO, not A
# A.ping


class E(C, B):
    def ping(self):
        print("E.ping")
        super().ping()


print("MRO of E:", E.mro())
# E -> C -> B -> A -> object  (parents swapped, MRO flips)

print("--- E().ping() ---")
E().ping()
# E.ping
# C.ping
# B.ping
# A.ping


# Without super(), the rest of MRO is skipped.
class X:
    def ping(self):
        print("X.ping")


class Y(X):
    def ping(self):
        print("Y.ping")
        # no super() — Z and X never run


class Z(X):
    def ping(self):
        print("Z.ping")
        super().ping()


class Broken(Y, Z):
    def ping(self):
        print("Broken.ping")
        super().ping()


print("MRO of Broken:", Broken.mro())
# Broken -> Y -> Z -> X -> object

print("--- Broken().ping() ---")
Broken().ping()
# Broken.ping
# Y.ping
# Z and X are skipped because Y.ping does not call super()
