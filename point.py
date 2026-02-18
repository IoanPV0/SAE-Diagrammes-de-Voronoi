import pygame
from config import screen
class Point():
    def __init__(self, abscisse : float, ordonnee : float):
        self.x : float = abscisse
        self.y : float = ordonnee

    @property
    def x(self) -> float:
        return self._x
    
    @property
    def y(self) -> float:
        return self._y
    
    @x.setter
    def x(self, abscisse : float) -> None:
        self._x = abscisse
    
    @y.setter
    def y(self, ordonnee : float) -> None:
        self._y = ordonnee
    
    def tracer(self) -> None:
        if self.y > 0 and self.y < screen.get_height():
            pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), 1)