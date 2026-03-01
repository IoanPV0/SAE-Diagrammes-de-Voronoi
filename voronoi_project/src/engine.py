import math
from typing import List, Tuple
from .models import Point
from .metrics import DistanceMetric, EuclideanDistance

class VoronoiEngine:
    """Moteur de calcul robuste et adaptatif."""
    
    def __init__(self, points: List[Point], padding: float = 2.0, metric: DistanceMetric = None):
        if not points:
            raise ValueError("La liste de points ne peut pas être vide.")
        
        self.points = points
        self.padding = padding
        self.metric = metric or EuclideanDistance()
        
        # On calcule les limites réelles pour l'affichage adaptatif
        self.min_x, self.max_x, self.min_y, self.max_y = self._compute_bounds()

    def _compute_bounds(self) -> Tuple[float, float, float, float]:
        """Détermine la zone d'étude en fonction des points + marge."""
        xs = [p.x for p in self.points]
        ys = [p.y for p in self.points]
        return (min(xs) - self.padding, max(xs) + self.padding, 
                min(ys) - self.padding, max(ys) + self.padding)

    def compute_map(self, resolution: int = 500) -> Tuple[List[List[int]], Tuple[float, float, float, float]]:
        """Génère la grille en respectant l'échelle réelle des points."""
        width_units = self.max_x - self.min_x
        height_units = self.max_y - self.min_y
        
        # Gestion du ratio d'aspect
        if width_units > height_units:
            w, h = resolution, int(resolution * (height_units / width_units))
        else:
            w, h = int(resolution * (width_units / height_units)), resolution

        grid = [[0 for _ in range(w)] for _ in range(h)]
        pts_coords = [(p.x, p.y) for p in self.points]

        for j in range(h):
            # Coordonnée Y réelle
            real_y = self.min_y + (j / h) * height_units
            for i in range(w):
                # Coordonnée X réelle
                real_x = self.min_x + (i / w) * width_units
                
                # Recherche du voisin le plus proche (Optimisé)
                min_dist = float('inf')
                closest_idx = 0
                for idx, (px, py) in enumerate(pts_coords):
                    # Utilisation de la distance au carré pour éviter math.sqrt (gain CPU)
                    dist_sq = (real_x - px)**2 + (real_y - py)**2
                    if dist_sq < min_dist:
                        min_dist = dist_sq
                        closest_idx = idx
                grid[j][i] = closest_idx
                
        return grid, (self.min_x, self.max_x, self.min_y, self.max_y)