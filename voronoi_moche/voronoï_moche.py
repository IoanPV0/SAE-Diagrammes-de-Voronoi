import matplotlib.pyplot as plt
import numpy as np
from point import Point
from json import load
from math import sqrt

#coucou les loulous ça marche !!!

def json_loader(chemin:str="liste_de_sites.json"):

    with open(chemin, "r", encoding="utf-8") as fp:
        données = load(fp)

    return données

def dictionnaire_germes(germes:list[Point], pixel:Point):
    dico_distances = {}
    for germe in germes: # À VOIR
        dico_distances[germe]=germe.distance_to(pixel)
    return dico_distances

def distance_minimale(dico_distances:dict[Point,float]):
    for germe, distance in dico_distances.items():
        if distance == min(dico_distances.values()):
            return germe

def germe_le_plus_proche(germes:list[Point], pixel:Point):
    dictionnaire_distances = dictionnaire_germes(germes, pixel)
    return distance_minimale(dictionnaire_distances)


def afficher_germe(germes:list[Point]):
    for germe in germes:
        plt.scatter(germe.x, germe.y, color='red', marker='x')

def coloriage(height, width, espacement, germes):

    voronoi_diagram = np.zeros((height,width))

    dico_couleur = {}
    c=0
    for germe in germes :
        dico_couleur[germe]=c
        c+=1

    for i in range(0,height,espacement):
        for j in range(0,width,espacement):
            voronoi_diagram[i][j] = dico_couleur[germe_le_plus_proche(germes, pixel = Point(j, i))]
        

    plt.imshow(voronoi_diagram,origin='lower')

            


def voronoi_moche(fig,liste_points:Point):
    pass

if __name__ == "__main__":
    
    fig = plt.figure()

    germes_exemple = [Point(2, 3),Point(98,34),Point(12,45),Point(34,56),Point(78,90),Point(23,67),Point(45,23),Point(56,78),Point(67,12),Point(89,34)]
    # exemple : on trace un grillage de 4×2 avec espacement 0.5
    #def_grillage(fig, width=10, height=10, spacing=1)
    afficher_germe(germes_exemple)
    coloriage(100,100,1,germes_exemple)

    plt.show()  # affiche le grillage
    #donnees_points_brutes = json_loader()
    #points = Points(donnees_points_brutes)
    #
    #afficher_point(fig,points)
    #
    #quadrillage_extremum = points.get_extrumum_points_of_cadrillage()
    #grillage(fig,quadrillage_extremum)
    #
    #voronoi_moche(fig,points)
    
    plt.savefig("matplotlib_grid_01.png", bbox_inches='tight')

    plt.close()