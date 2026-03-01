import sys
import matplotlib.pyplot as plt
from src.io_handler import FileHandler
from src.engine import VoronoiEngine
from src.benchmark import VoronoiBenchmark

sys.setrecursionlimit(2000)

def run_app(file_path: str):
    points = FileHandler.read_points_from_file(file_path)
    
    # Initialisation du moteur (il calcule ses propres limites)
    engine = VoronoiEngine(points, padding=2.0)
    
    # Calcul de la carte (500 pixels de côté pour la précision)
    voronoi_map, bounds = engine.compute_map(resolution=500)
    min_x, max_x, min_y, max_y = bounds

    # Visualisation avec les vraies échelles
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # L'argument 'extent' replace la grille de pixels dans l'espace mathématique réel
    ax.imshow(voronoi_map, 
              extent=(min_x, max_x, min_y, max_y), 
              origin='lower', 
              cmap='terrain', 
              alpha=0.7)

    # Dessin des points sources
    ax.scatter([p.x for p in points], [p.y for p in points], 
               c='red', edgecolors='black', zorder=5)

    ax.set_title(f"Voronoi Adaptatif - Echelle: [{min_x:.1f}:{max_x:.1f}]")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.show()

def run_benchmark_mode():
    """Lance une analyse de performance automatique."""
    print("--- Mode Benchmark ---")
    bench = VoronoiBenchmark()
    # Teste pour 5, 20, 50 et 100 points
    bench.run_suite(sizes=[5, 20, 50, 100], resolution=400)

if __name__ == "__main__":
    run_app("data.txt")
    # run_benchmark_mode()