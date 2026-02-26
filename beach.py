from circle import Circle
from parabole_service import *
from segment import Segment
from typing import Union

class Beach():
    '''
    La plage formée par les arcs de paraboles
    '''
    def __init__ (self):
        self._liste_points: list[Point] = [] # c'est la plage formée par une suite de foyers
        self._liste_segments_en_cours: list[Segment] = [] # les intersections
        self._liste_segment_finis: list[Segment] = [] # quand les intersections se rejoingnent (cercle)

    def insert_point(self, point:Point):
        '''
        insère un point dans la plage
        '''
        print("-----------------------------------------------------")
        print("insertion du point ", point)
        print("plage avant insertion ", self._liste_points)
        print("liste des segments en cours avant insertion ", self._liste_segments_en_cours)
        print("liste des segments finis avant insertion ", self._liste_segment_finis)
        if self._liste_points == []:
            self._liste_points.append(point)
        elif len(self._liste_points) == 1:
                self._liste_points.append(point)
                self._liste_points.append(self._liste_points[0])
                self._liste_segments_en_cours.append(Segment(Point(get_x(self._liste_points[0], point.y, point.x), point.y)))
                self._liste_segments_en_cours.append(Segment(Point(get_x(self._liste_points[0], point.y, point.x), point.y)))
        else:
            for i in range(len(self._liste_points)-1):
                    print("on est dans la boucle, i = ", i)
                    inter = intersection(self._liste_points[i], self._liste_points[i+1], point.x)
                    if inter.y < point.y: #retravailler cette condition
                        print(i,inter.y,point.y)
                        continue
                        
                    if inter.y > point.y:
                        print("on est ici, i = ", i)
                        self._liste_points.insert(i+1, point)
                        self._liste_points.insert(i+2, self._liste_points[i])
                        point_start_segment = Point(get_x(self._liste_points[i], point.y, point.x), point.y)
                        self._liste_segments_en_cours.insert(i,Segment(point_start_segment))
                        self._liste_segments_en_cours.insert(i,Segment(point_start_segment))
                        return
                    else:
                        print("on est là i = ", i)
                        self._liste_points.append(point)
                        self._liste_points.append(self._liste_points[i])
                        point_start_segment = Point(get_x(self._liste_points[i], point.y, point.x), point.y)
                        self._liste_segments_en_cours.insert(i,Segment(point_start_segment))
                        self._liste_segments_en_cours.insert(i,Segment(point_start_segment))
                        return
    
    
    def detecte_cercle_valable(self, nouveau_foyer:Point):
        '''
        teste les cercles valables autour de la plage
        '''
        print("points à tester pour les cercles : ", self._liste_points)
        cercles = []
        if len(self._liste_points) < 3:
            return []
        for i in range(len(self._liste_points)-2):
            if Circle.points_valid(self._liste_points[i], self._liste_points[i+1], self._liste_points[i+2]):
                cercles.append(Circle(self._liste_points[i], self._liste_points[i+1], self._liste_points[i+2]))
        return cercles
    
    def insert_cercle(self, cercle:Circle):
        '''
        insère un cercle dans la plage
        '''
        print(f"insertion du {cercle}")
        #trouver le point du cercle qui a le plus grand x
        A = cercle._A
        B = cercle._B
        C = cercle._C
        if A.x > B.x and A.x > C.x:
            point_droite = A
        elif B.x > A.x and B.x > C.x:
            point_droite = B
        else:
            point_droite = C

        circles = self.detecte_cercle_valable(point_droite)
        print("cercles valables : ", circles)
        if circles != []:
            return circles
        return None

    def refermer_segments (self, cercle:Circle):
        print(f"réfermer les segments pour le {cercle}")
        centre = cercle.center
        #trouver le point du cercle qui a le plus grand x
        A = cercle._A
        B = cercle._B
        C = cercle._C
        #il faut parcourir les point de départ des segments et trouver les origines qui encadre le y du centre du cercle
        for i in range(len(self._liste_points)-2):
            if self._liste_points[i] == A and self._liste_points[i+1] == B and self._liste_points[i+2] == C:
                print(self._liste_segments_en_cours)
                self._liste_segments_en_cours[i].finish(centre)
                self._liste_segments_en_cours[i+1].finish(centre)
                #il faut ajouter les deux segments dans la liste des segments finis
                self._liste_segment_finis.append(self._liste_segments_en_cours[i])
                self._liste_segment_finis.append(self._liste_segments_en_cours[i+1])
                #supprimer les 2 segments qu'on vient d'ajouter dans la liste des segments finis
                del self._liste_segments_en_cours[i]
                del self._liste_segments_en_cours[i]
                del self._liste_points[i+1]
                #on ajoute un segments pour boucher le trou             
                self._liste_segments_en_cours.append(Segment(centre))
                
