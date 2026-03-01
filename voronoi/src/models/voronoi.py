# src/models/voronoi.py
import math
from typing import List, Tuple, Set, Dict
from .point import Point
from .edge import Edge

class VoronoiDiagram:
    def __init__(self, points: List[Point]):
        self.points = points
        self.edges: List[Edge] = []
        self._triangles = []

    def build(self):
        if len(self.points) < 2:
            return

        # 1. Créer un super-triangle
        super_triangle = self._create_super_triangle()
        self._triangles = [super_triangle]

        # 2. Ajouter chaque point
        for point in self.points:
            bad_triangles = []
            for triangle in self._triangles:
                if self._is_point_in_circumcircle(point, triangle):
                    bad_triangles.append(triangle)

            polygon = self._find_polygon_hole(bad_triangles)
            for triangle in bad_triangles:
                self._triangles.remove(triangle)

            for edge in polygon:
                new_triangle = (edge[0], edge[1], point)
                self._triangles.append(new_triangle)

        # 3. Supprimer les triangles avec le super-triangle
        self._remove_super_triangle_edges(super_triangle)
        # 4. Générer les arêtes de Voronoï
        self._generate_voronoi_edges()

    def _create_super_triangle(self) -> Tuple[Point, Point, Point]:
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
        a, b, c = triangle
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
        edges = []
        for triangle in bad_triangles:
            edges.extend([(triangle[0], triangle[1]), (triangle[1], triangle[2]), (triangle[2], triangle[0])])
        polygon = []
        for edge in edges:
            if edges.count((edge[1], edge[0])) == 0 and edges.count(edge) == 1:
                polygon.append(edge)
        return polygon

    def _remove_super_triangle_edges(self, super_triangle: Tuple[Point, Point, Point]):
        self._triangles = [t for t in self._triangles if not any(p in super_triangle for p in t)]

    def _generate_voronoi_edges(self):
        """Génère les arêtes de Voronoï à partir des triangles de Delaunay."""
        # Dictionnaire pour stocker les centres des cercles circonscrits
        circumcenters = {}

        # Pour chaque triangle, calculer le centre du cercle circonscrit
        for triangle in self._triangles:
            a, b, c = triangle
            center = self._circumcenter(a, b, c)
            circumcenters[(a, b, c)] = center

        # Pour chaque arête de Delaunay, relier les centres des cercles adjacents
        edge_to_centers = {}
        for triangle in self._triangles:
            a, b, c = triangle
            center = circumcenters[(a, b, c)]
            for i in range(3):
                edge = (triangle[i], triangle[(i+1)%3])
                if edge not in edge_to_centers:
                    edge_to_centers[edge] = []
                edge_to_centers[edge].append(center)

        # Les arêtes de Voronoï sont les segments reliant les centres des cercles adjacents
        for edge, centers in edge_to_centers.items():
            if len(centers) == 2:
                self.edges.append(Edge(centers[0], centers[1]))

    def _circumcenter(self, a: Point, b: Point, c: Point) -> Point:
        """Calcule le centre du cercle circonscrit d'un triangle."""
        # Calcul des milieux et des pentes
        d = 2 * (a.x * (b.y - c.y) + b.x * (c.y - a.y) + c.x * (a.y - b.y))
        if d == 0:
            return Point(float('inf'), float('inf'))  # Points colinéaires

        ux = ((a.x**2 + a.y**2) * (b.y - c.y) + (b.x**2 + b.y**2) * (c.y - a.y) + (c.x**2 + c.y**2) * (a.y - b.y)) / d
        uy = ((a.x**2 + a.y**2) * (c.x - b.x) + (b.x**2 + b.y**2) * (a.x - c.x) + (c.x**2 + c.y**2) * (b.x - a.x)) / d
        return Point(ux, uy)

    def get_edges(self) -> List[Edge]:
        return self.edges
