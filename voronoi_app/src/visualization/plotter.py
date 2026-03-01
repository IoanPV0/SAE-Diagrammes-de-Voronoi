import matplotlib.pyplot as plt
from src.models.voronoi_diagram import VoronoiDiagram
from src.models.point import Point

class VoronoiPlotter:
    """Responsabilité unique : visualisation et export."""

    @staticmethod
    def plot(diagram: VoronoiDiagram, title: str = "Diagramme de Voronoï") -> plt.Figure:
        fig, ax = plt.subplots(figsize=(10, 8))
        # Sites
        xs = [p.x for p in diagram.sites]
        ys = [p.y for p in diagram.sites]
        ax.scatter(xs, ys, c='red', s=50, label='Sites', zorder=5)

        # Arêtes Voronoï
        for start, end in diagram.edges:
            ax.plot([start.x, end.x], [start.y, end.y], 'b-', linewidth=1.5, alpha=0.8)

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_title(title)
        ax.legend()
        ax.grid(True, alpha=0.3)
        return fig

    @staticmethod
    def save(fig: plt.Figure, filename: str) -> None:
        """Export SVG ou PNG selon extension."""
        fig.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close(fig)