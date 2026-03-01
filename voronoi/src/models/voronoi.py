from typing import List
from .point import Point
from .edge import Edge

class VoronoiDiagram:
    """Représente un diagramme de Voronoï, construit à partir d'une liste de points."""

    def __init__(self, points: List[Point]):
        self.points = points
        self.edges: List[Edge] = []

    def build(self):
        """Construit le diagramme de Voronoï à partir des points."""
        # TODO: Implémenter l'algorithme de Fortune ou Bowyer-Watson ici
        # Pour l'instant, on retourne un diagramme vide pour l'exemple
        pass

    def get_edges(self) -> List[Edge]:
        """Retourne la liste des arêtes du diagramme."""
        return self.edges
