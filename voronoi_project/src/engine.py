import math
from typing import List, Tuple
from .models import Point

class VoronoiEngine:
    """Moteur de calcul adaptatif pour le diagramme de Voronoï."""
    
    def __init__(self, points: List[Point], padding: float = 10.0):
        if not points:
            raise ValueError("La liste de points ne peut pas être vide.")
        self.points = points
        self.padding = padding
        # On calcule les limites dès l'initialisation (Principe d'expert)
        self.min_x, self.max_x, self.min_y, self.max_y = self._compute_bounds()

    def _compute_bounds(self) -> Tuple[float, float, float, float]:
        """Calcule les limites du plan en fonction des points + une marge."""
        xs = [p.x for p in self.points]
        ys = [p.y for p in self.points]
        return (min(xs) - self.padding, max(xs) + self.padding, 
                min(ys) - self.padding, max(ys) + self.padding)

    def compute_map(self, resolution: int = 500) -> Tuple[List[List[int]], Tuple[float, float, float, float]]:
        """
        Génère une matrice proportionnelle à l'échelle des points.
        resolution: nombre de divisions sur l'axe le plus long.
        """
        width_units = self.max_x - self.min_x
        height_units = self.max_y - self.min_y
        
        # On garde le ratio d'aspect (Aspect Ratio) pour ne pas déformer le diagramme
        if width_units > height_units:
            w, h = resolution, int(resolution * (height_units / width_units))
        else:
            w, h = int(resolution * (width_units / height_units)), resolution

        grid = [[0 for _ in range(w)] for _ in range(h)]
        
        for j in range(h):
            for i in range(w):
                # Conversion coordonnée pixel -> coordonnée réelle (Scaling)
                real_x = self.min_x + (i / w) * width_units
                real_y = self.min_y + (j / h) * height_units
                grid[j][i] = self.get_closest_point_index(Point(real_x, real_y))
        
        return grid, (self.min_x, self.max_x, self.min_y, self.max_y)

    def get_closest_point_index(self, target: Point) -> int:
        """Trouve l'indice du point le plus proche (inchangé)."""
        min_dist = float('inf')
        closest_idx = -1
        for i, p in enumerate(self.points):
            dist = target.distance_to(p)
            if dist < min_dist:
                min_dist = dist
                closest_idx = i
        return closest_idx