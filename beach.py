from circle import Circle
from parabole_service import *
from segment import Segment
from typing import Union

class Beach():
    '''
    La plage formée par les arcs de paraboles
    '''
    def __init__ (self):
        self._liste_points: list[Union[Point, Circle]] = []
        self._liste_segments_en_cours: list[Segment] = []
        self._liste_segment_finis: list[Segment] = []

    def insert_point(self, point:Point, sites:list[Point]):
        '''
        insère un point dans la plage
        '''
        if self._liste_points == []:
            self._liste_points.append(point)
        else:  
            if len(self._liste_points) == 1:
                self._liste_points.append(point)
                self._liste_points.append(self._liste_points[0])
                inter = Point((self._liste_points[0].x + point.x)/2, self._liste_points[0].y)
                self._liste_segments_en_cours.append(Segment(inter))
                self._liste_segments_en_cours.append(Segment(inter))

            else:
                sites_points = [p for p in sites if p.x < point.x]
                for i in range(len(sites_points)-1):
                    inter = intersection(sites_points[i],sites_points[i+1], point.x)
                    if inter.y > point.y :
                        break
                    if inter.y < point.y :
                        self._liste_points.insert(i+1, inter)
                        self._liste_segments_en_cours.append(Segment(inter))
                        self._liste_segments_en_cours.append(Segment(inter))
    
    def detecte_cercle_valable(self, sites:list[Point], x_line:float = None):
        '''
        teste les cercles valables autour de la plage
        '''
        sites_points = [p for p in sites if p.x < x_line]
        cercles = []
        if len(sites_points) < 3:
            return []
        for i in range(len(sites_points)-2):
            if Circle.points_valid(sites_points[i], sites_points[i+1], sites_points[i+2]):
                cercles.append(Circle(sites_points[i], sites_points[i+1], sites_points[i+2]))
        return cercles
    
    def insert_cercle(self, sites:list[Point], x_line:float = None):
        '''
        insère un cercle dans la plage
        '''
        circles = self.detecte_cercle_valable(sites, x_line)
        if circles != []:
            return circles
        return None

    def refermer_segments (self, cercle:Circle):
        cercle._calc_centre_rayon()
        centre = cercle.center
        #il faut parcourir les point de départ des ssegments et trouver les origines qui encadre le y du centre du cercle
        for i in range(len(self._liste_segments_en_cours)):
            if self._liste_segments_en_cours[i].points[0].y < centre.y and self._liste_segments_en_cours[i+1].points[0].y > centre.y:
                #on referme les segment et on les enlève de la liste en cours pour les mettre dans la liste des segments finis
                self._liste_segment_finis.append(Segment(self._liste_segments_en_cours[i].points[0], centre))
                self._liste_segment_finis.append(Segment(self._liste_segments_en_cours[i+1].points[0], centre))
                print(self._liste_segment_finis)
                #supprimer les 2 segments qu'on vient d'ajouter dans la liste des segments finis
                del self._liste_segments_en_cours[i:i+2]
                #on ajoute deux segments pour boucher le trou laissé par les segments fermés
                #un qui démarre au centre du cercle et n'ap pas de fin, et l'autre qui commence au point qui n'est le centre parmis les deux poins qui composnt les segments qui ont été fermés
                if self._liste_segments_en_cours[i].points[0].y < max(cercle.points[0].y, cercle.points[2].y):
                    autre_point = self._liste_segments_en_cours[i].points[0]
                else :
                    autre_point = self._liste_segments_en_cours[i+1].points[0]
                
                self._liste_segments_en_cours.append(Segment(centre), Segment(autre_point))