import os
from typing import List
from .models import Point

class FileHandler:
    """Gère la lecture des coordonnées et les exports."""

    @staticmethod
    def read_points_from_file(filepath: str) -> List[Point]:
        """Lit un fichier texte et extrait les points."""
        points = []
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Le fichier {filepath} est introuvable.")

        with open(filepath, 'r') as f:
            for line_num, line in enumerate(f, 1):
                clean_line = line.strip().replace(',', ' ')
                if not clean_line: continue
                
                try:
                    parts = clean_line.split()
                    if len(parts) != 2:
                        raise ValueError(f"Format invalide ligne {line_num}")
                    points.append(Point(float(parts[0]), float(parts[1])))
                except ValueError as e:
                    print(f"Erreur de parsing ligne {line_num}: {e}")
        return points

    @staticmethod
    def export_to_svg(points: List[Point], voronoi_map: List[List[int]], bounds: tuple, filename: str):
            """Exporte une représentation visuelle du diagramme en SVG."""
            min_x, max_x, min_y, max_y = bounds
            width = max_x - min_x
            height = max_y - min_y
            
            # On définit une échelle pour que le SVG soit lisible (ex: 500px de large)
            view_scale = 500 / width if width > 0 else 1
            svg_w = width * view_scale
            svg_h = height * view_scale

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f'<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
                f.write(f'<svg width="{svg_w}" height="{svg_h}" viewBox="0 0 {svg_w} {svg_h}" xmlns="http://www.w3.org/2000/svg">\n')
                
                # Fond
                f.write(f'  <rect width="100%" height="100%" fill="#f0f0f0" />\n')

                # Dessin des points
                for p in points:
                    # On translate les coordonnées pour qu'elles rentrent dans le cadre SVG
                    cx = (p.x - min_x) * view_scale
                    cy = svg_h - ((p.y - min_y) * view_scale) # Inversion Y pour le standard SVG
                    f.write(f'  <circle cx="{cx}" cy="{cy}" r="4" fill="red" stroke="black" stroke-width="1" />\n')
                
                f.write('</svg>')
            print(f"Export SVG réussi : {filename}")