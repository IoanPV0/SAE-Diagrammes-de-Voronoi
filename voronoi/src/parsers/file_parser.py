from typing import List
from src.models.point import Point

class FileParser:
    """Parse un fichier texte contenant des points sous forme de paires de coordonnées."""

    @staticmethod
    def parse(file_path: str) -> List[Point]:
        """Parse le fichier et retourne une liste de points."""
        points = []
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    x, y = map(float, line.split(','))
                    points.append(Point(x, y))
                except ValueError:
                    raise ValueError(f"Format invalide: '{line}'. Attendu: x,y")
        return points
