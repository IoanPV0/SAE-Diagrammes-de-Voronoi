from typing import List
from ..models.voronoi import VoronoiDiagram

class SVGVisualizer:
    """Génère une représentation SVG du diagramme de Voronoï."""

    @staticmethod
    def visualize(diagram: VoronoiDiagram, output_path: str):
        """Génère un fichier SVG à partir du diagramme."""
        # TODO: Implémenter la génération SVG
        with open(output_path, 'w') as f:
            f.write("<svg xmlns='http://www.w3.org/2000/svg' width='500' height='500'>\n")
            f.write("</svg>\n")
