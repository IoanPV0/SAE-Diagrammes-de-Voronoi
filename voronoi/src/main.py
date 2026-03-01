from parsers.file_parser import FileParser
from services.voronoi_builder import VoronoiBuilder
from services.performance_meter import PerformanceMeter
from visualizers.svg_visualizer import SVGVisualizer

def main():
    file_path = "example_points.txt"
    output_svg = "voronoi.svg"

    # Parse les points
    points = FileParser.parse(file_path)

    # Mesure la performance
    time_taken = PerformanceMeter.measure(VoronoiBuilder.build, points)
    print(f"Temps d'exécution: {time_taken:.4f} secondes")

    # Construit le diagramme
    diagram = VoronoiBuilder.build(points)

    # Visualise
    SVGVisualizer.visualize(diagram, output_svg)

if __name__ == "__main__":
    main()
