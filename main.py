import pygame
from droite import Droite
from point import Point
from parabole import Parabole
from config import screen, clock
screen.fill((255, 255, 255))

droite = Droite(300)
droite.tracer()


foyer1 = Point(250, 200)
foyer1.tracer()

foyer2 = Point(230, 275)
foyer2.tracer()

parabole1 = Parabole(foyer1, droite)
parabole1.tracer()

parabole2 = Parabole(foyer2, droite)
parabole2.tracer()

intersection = parabole1.intersection(parabole2)
for point in intersection:
    point.tracer((255,0,0))

pygame.display.flip()


running = True
while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            