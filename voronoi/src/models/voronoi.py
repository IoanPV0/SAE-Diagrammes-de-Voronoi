import math
from typing import List, Tuple
from src.models.point import Point
from src.models.edge import Edge

class VoronoiDiagram:
    """Représente un diagramme de Voronoï, construit à partir d'une liste de points."""

    def __init__(self, points: List[Point]):
        self.points = points
        self.edges: List[Edge] = []
        self._triangles = []

    def build(self):
        """Construit le diagramme de Voronoï à partir des points (algorithme Bowyer-Watson)."""
        if len(self.points) < 2:
            return

        # 1. Créer un super-triangle contenant tous les points
        super_triangle = self._create_super_triangle()
        self._triangles = [super_triangle]

        # 2. Ajouter chaque point un par un
        for point in self.points:
            bad_triangles = []
            # Trouver tous les triangles dont le cercle circonscrit contient le point
            for triangle in self._triangles:
                if self._is_point_in_circumcircle(point, triangle):
                    bad_triangles.append(triangle)
            # Trouver la frontière de la cavité
            polygon = self._find_polygon_hole(bad_triangles)
            # Supprimer les mauvais triangles
            for triangle in bad_triangles:
                self._triangles.remove(triangle)
            # Remplir la cavité avec de nouveaux triangles
            for edge in polygon:
                new_triangle = (edge[0], edge[1], point)
                self._triangles.append(new_triangle)

        # 3. Supprimer les triangles contenant des sommets du super-triangle
        self._remove_super_triangle_edges(super_triangle)
        # 4. Extraire les arêtes de Voronoï
        self._extract_voronoi_edges()

    def _create_super_triangle(self) -> Tuple[Point, Point, Point]:
        """Crée un triangle suffisamment grand pour contenir tous les points."""
        min_x = min(p.x for p in self.points) - 10
        min_y = min(p.y for p in self.points) - 10
        max_x = max(p.x for p in self.points) + 10
        max_y = max(p.y for p in self.points) + 10
        dx = max_x - min_x
        dy = max_y - min_y
        return (
            Point(min_x - dx, min_y - dy),
            Point(min_x - dx, max_y + dy),
            Point(max_x + dx, min_y - dy)
        )

    def _is_point_in_circumcircle(self, point: Point, triangle: Tuple[Point, Point, Point]) -> bool:
        """Teste si un point est à l'intérieur du cercle circonscrit d'un triangle."""
        a, b, c = triangle
        # Calcul du déterminant pour le test du cercle circonscrit
        # (voir formule mathématique standard)
        return (
            (a.x**2 + a.y**2) * (b.y - c.y) +
            (b.x**2 + b.y**2) * (c.y - a.y) +
            (c.x**2 + c.y**2) * (a.y - b.y) -
            point.x**2 * (b.y - c.y) -
            point.y**2 * (b.x - c.x) -
            (a.x**2 + a.y**2) * (b.x - c.x) -
            (b.x**2 + b.y**2) * (c.x - a.x) -
            (c.x**2 + c.y**2) * (a.x - b.x) -
            point.x**2 * (c.y - a.y) -
            point.y**2 * (a.x - b.x)
        ) > 0

    def _find_polygon_hole(self, bad_triangles: List[Tuple[Point, Point, Point]]) -> List[Tuple[Point, Point]]:
        """Trouve la frontière de la cavité formée par les mauvais triangles."""
        edges = []
        for triangle in bad_triangles:
            edges.extend([(triangle[0], triangle[1]), (triangle[1], triangle[2]), (triangle[2], triangle[0])])
        polygon = []
        for edge in edges:
            if edges.count((edge[1], edge[0])) == 0 and edges.count(edge) == 1:
                polygon.append(edge)
        return polygon

    def _remove_super_triangle_edges(self, super_triangle: Tuple[Point, Point, Point]):
        """Supprime les arêtes liées au super-triangle."""
        self._triangles = [t for t in self._triangles if not any(p in super_triangle for p in t)]

    def _extract_voronoi_edges(self):
        """Extrait les arêtes de Voronoï à partir des triangles de Delaunay."""
        edge_map = {}
        for triangle in self._triangles:
            for i in range(3):
                edge = (triangle[i], triangle[(i+1)%3])
                if edge in edge_map:
                    edge_map[edge] += 1
                else:
                    edge_map[(edge[1], edge[0])] = 1
        for edge, count in edge_map.items():
            if count == 1:
                self.edges.append(Edge(edge[0], edge[1]))

    def get_edges(self) -> List[Edge]:
        """Retourne la liste des arêtes du diagramme."""
        return self.edges
