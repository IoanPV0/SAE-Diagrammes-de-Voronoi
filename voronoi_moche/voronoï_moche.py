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
    for germe in germes:
        dico_distances[germe]=germe.distance_to(pixel)
    return dico_distances

def distance_minimale(dico_distances:dict[Point,float]):
    for germe, distance in dico_distances.items():
        if distance == min(dico_distances.values()):
            return germe

def germe_le_plus_proche(germes:list[Point], pixel:Point):
    dictionnaire_distances = dictionnaire_germes(germes, pixel)
    return distance_minimale(dictionnaire_distances)


#def coloriage():

#A REFAIRE
def def_grillage(fig, width: float, height: float, spacing: float = 0.1):
    ax = fig.add_subplot(1, 1, 1)

    plt.xlim(0, width)
    plt.ylim(0, height)

    grid_x_ticks = np.arange(0, width, spacing)
    grid_y_ticks = np.arange(0, height, spacing)

    ax.set_xticks(grid_x_ticks, minor=True)
    ax.set_yticks(grid_y_ticks, minor=True)

    ax.grid(which='both')
    ax.grid(which='minor', alpha=0.2, linestyle='--')

#A REFAIRE
def afficher_germe(germes:list[Point]):
    for germe in germes:
        plt.scatter(germe.x, germe.y, color='red', marker='x')



def voronoi_moche(fig,liste_points:Point):
    pass

if __name__ == "__main__":
    
    fig = plt.figure()

    # exemple : on trace un grillage de 4×2 avec espacement 0.5
    def_grillage(fig, width=10, height=10, spacing=1)
    afficher_germe([Point(2, 3), Point(7, 8), Point(5, 5)])

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