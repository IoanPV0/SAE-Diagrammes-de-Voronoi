from point import Point
from droite import Droite
from config import screen
from math import sqrt
class Parabole():
    def __init__(self, foyer : Point, directrice : Droite):
        self.foyer = foyer
        self.directrice = directrice
        self.domaine = None

    def calcul_domaine(self) -> None:
        a = self.foyer.x
        k = self.directrice.x
        # foyer et parabole à droite de la directrice
        if a > k: 
            self.domaine = (int((a + k) / 2), int(screen.get_width()))
        # foyer et parabole à gauche de la directrice
        else: 
            self.domaine = (int(0), int((a + k) / 2))
        

    def equation(self, x: float) -> list[Point]:
        a = self.foyer.x
        b = self.foyer.y
        k = self.directrice.x

        # equation de départ pour une directrice verticale : 
        # (y - b)**2 = 2(a - k)*x + (k**2 - a**2)
        # la partie sous la racine carrée de droite doit être positive ou 
        # nulle pour que y soit réel
        
        discriminant = 2 * (a - k) * x + (k**2 - a**2)

        # verification si le discriminant est négatif
        if discriminant < 0:
            return []

        y1 = b + sqrt(discriminant)
        y2 = b - sqrt(discriminant)
        p1 = Point(x, y1)
        p2 = Point(x, y2)
        return [p1, p2]

            

    def intersection(self, parabole) -> list[Point]:
        pass
            

    def tracer(self) -> None:
        # calcul du domaine de définition de x
        self.calcul_domaine()
        for abscisse in range(self.domaine[0], self.domaine[1] * 100):
            x = abscisse * 0.01
            points = self.equation(x)
            if points != []:
                for point in points:
                    point.tracer()
