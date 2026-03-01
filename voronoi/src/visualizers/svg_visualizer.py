from typing import List
from models.voronoi import VoronoiDiagram
from models.edge import Edge

class SVGVisualizer:
    """Génère une représentation SVG d'un diagramme de Voronoï."""

    @staticmethod
    def visualize(diagram: VoronoiDiagram, output_path: str):
        """Génère un fichier SVG du diagramme de Voronoï."""
        edges = diagram.get_edges()
        points = diagram.points
        min_x = min(p.x for p in points) - 1
        min_y = min(p.y for p in points) - 1
        max_x = max(p.x for p in points) + 1
        max_y = max(p.y for p in points) + 1
        width = 500
        height = 500

        def scale_x(x: float) -> float:
            return ((x - min_x) / (max_x - min_x)) * width

        def scale_y(y: float) -> float:
            return height - ((y - min_y) / (max_y - min_y)) * height

        with open(output_path, 'w') as f:
            f.write(f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">\n')
            # Dessiner les arêtes de Voronoï
            for edge in edges:
                x1, y1 = scale_x(edge.start.x), scale_y(edge.start.y)
                x2, y2 = scale_x(edge.end.x), scale_y(edge.end.y)
                f.write(f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="black" stroke-width="1" />\n')
            # Dessiner les points
            for point in points:
                x, y = scale_x(point.x), scale_y(point.y)
                f.write(f'  <circle cx="{x}" cy="{y}" r="3" fill="red" />\n')
            f.write('</svg>\n')
