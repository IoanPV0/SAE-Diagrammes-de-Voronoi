from typing import List
from src.models.point import Point
from src.models.voronoi import VoronoiDiagram

class VoronoiBuilder:
    """Service pour construire un diagramme de Voronoï à partir d'une liste de points."""

    @staticmethod
    def build(points: List[Point]) -> VoronoiDiagram:
        """Construit et retourne un diagramme de Voronoï."""
        diagram = VoronoiDiagram(points)
        diagram.build()
        return diagram
