from pathlib import Path
from typing import List
from src.models.point import Point

class FileHandler:
    """Responsabilité : lecture/écriture des fichiers de points."""

    @staticmethod
    def read_points(file_path: str | Path) -> List[Point]:
        """Lit un fichier .txt de points (une paire par ligne)."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Fichier non trouvé : {path}")
        points = []
        with path.open(encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                try:
                    x_str, y_str = line.split(",")
                    p = Point(float(x_str.strip()), float(y_str.strip()))
                    points.append(p)
                except Exception as e:
                    raise ValueError(f"Erreur ligne {line_num} : {line}") from e
        if len(points) < 2:
            raise ValueError("Le fichier doit contenir au moins 2 points.")
        return points

    @staticmethod
    def save_points(points: List[Point], file_path: str | Path) -> None:
        """(Optionnel) Sauvegarde points."""
        with Path(file_path).open("w", encoding="utf-8") as f:
            for p in points:
                f.write(f"{p.x},{p.y}\n")