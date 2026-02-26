from json_loader import load_json, convert_to_points
from point import Point
from priorityqueue import PriorityQueue
from parabole_service import *
from beach import Beach
import matplotlib.pyplot as plt


if __name__ == "__main__":
    data = load_json("liste_de_sites.json")
    sites = convert_to_points(data)
    plot_cadre = (Point(min(p.x for p in sites) - 10.0, min(p.y for p in sites) - 10.0), Point(max(p.x for p in sites) + 10.0, max(p.y for p in sites) + 10.0))
    queue:PriorityQueue = PriorityQueue()
    for point in sites:
        queue.push(point)
    beach = Beach()
    cercle_traites = []
    while not queue.empty():
        print(queue)
        event = queue.pop()
        if type(event) == Point:
            beach.insert_point(event)
            new_circles = beach.detecte_cercle_valable(event)
            if new_circles is not None:
                for circle in new_circles:
                    if circle not in queue._events:
                        queue.push(circle)
        else:
            cercle_traites.append(event)
            beach.refermer_segments(event)
            new_circles = beach.insert_cercle(event)
            if new_circles is not None:
                for circle in new_circles:
                    if circle not in cercle_traites and circle not in queue._events:
                        queue.push(circle)


    nuage = sites
    print(sites)
    segs = beach._liste_segment_finis
    print(segs)
    # en supposant que nuage est la liste de Point du diagramme
    xs_nuage = [pt.x for pt in nuage]
    ys_nuage = [pt.y for pt in nuage]
    plt.scatter(xs_nuage, ys_nuage)

    # en supposant que segs est la liste des segments
    for s in segs:
        p1, p2 = s.points
        plt.plot([p1.x, p2.x], [p1.y, p2.y])

    # zoom sur la zone utile, en supposant que
    # left, right, top, bottom définissent le cadre
    plt.xlim(plot_cadre[0].x, plot_cadre[1].x)
    plt.ylim(plot_cadre[0].y, plot_cadre[1].y)
        
    # orthonormé :
    ax = plt.gca()
    ax.set_aspect(1)

    # affichage
    plt.show()