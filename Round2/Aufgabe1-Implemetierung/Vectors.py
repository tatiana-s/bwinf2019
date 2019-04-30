import math

# Vektormethoden zur Anwending auf Koordinaten (R^2)


# Vektor zwischen 2 Koordinatenpunkten
def get_vector(c1, c2):
    vector = Coord()
    vector.set_x(c2.x - c1.x)
    vector.set_y(c2.y - c1.y)
    return vector


# Skalarprodukt
def dot_product(c1, c2):
    return c1.x*c2.x + c1.y*c2.y


# Betrag eines Vektors
def norm(v):
    return math.sqrt((v.x ** 2) + (v.y ** 2))


# Winkel zwischen 2 Vektoren
def compute_angle(v1, v2):
    alpha = math.acos(dot_product(v1, v2)/(norm(v1)*norm(v2)))
    return math.degrees(alpha)


# Länge des aus zwei 2-dimensionalen Vektoren durch Kreuzprodukt entstehenden senkrechten Vektors
def cross_product_direction(v1, v2):
    return v1.x*v2.y - v1.y*v2.x


# Koordinatenklasse zur besseren Handhabung von x und y Werten, inklusive Vektormethoden
class Coord:
    def __init__(self, pos_x=0, pos_y=0):
        self.x = pos_x
        self.y = pos_y

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def __str__(self):
        return "({}|{})".format(self.x, self.y)

    def __repr__(self):
        return "({}|{})".format(self.x, self.y)


