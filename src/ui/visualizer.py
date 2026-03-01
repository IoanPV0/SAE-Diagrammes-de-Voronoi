"""
Module de visualisation interactive des diagrammes.

Ce module fournit une interface de visualisation utilisant matplotlib
pour afficher les diagrammes de Voronoï de manière interactive.
"""

import matplotlib
matplotlib.use('TkAgg')  # Backend interactif pour Windows
import matplotlib.pyplot as plt
from src.domain.voronoi_diagram import VoronoiDiagram


class Visualizer:
    """
    Visualiseur interactif de diagrammes de Voronoï.
    
    Cette classe permet d'afficher les diagrammes dans une fenêtre
    interactive matplotlib.
    """
    
    def __init__(self, width: int = 10, height: int = 8) -> None:
        """
        Initialise le visualiseur.
        
        Args:
            width: Largeur de la figure en pouces (défaut: 10).
            height: Hauteur de la figure en pouces (défaut: 8).
        """
        self._width = width
        self._height = height
    
    def visualize(self, diagram: VoronoiDiagram, title: str = None) -> None:
        """
        Affiche le diagramme dans une fenêtre interactive.
        
        Args:
            diagram: Le diagramme à visualiser.
            title: Titre personnalisé (optionnel).
        """
        # Créer la figure
        fig, ax = plt.subplots(figsize=(self._width, self._height))
        
        # Dessiner le diagramme
        self._draw_diagram(ax, diagram)
        
        # Configurer l'apparence
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3, linestyle='--')
        
        # Titre
        if title is None:
            title = f'Diagramme de Voronoï - {len(diagram.sites)} sites'
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        
        # Labels
        ax.set_xlabel('X', fontsize=12)
        ax.set_ylabel('Y', fontsize=12)
        
        # Ajuster la disposition
        plt.tight_layout()
        
        # Afficher
        plt.show()
    
    def _draw_diagram(self, ax, diagram: VoronoiDiagram) -> None:
        """
        Dessine le diagramme sur un axe matplotlib.
        
        Args:
            ax: L'axe matplotlib sur lequel dessiner.
            diagram: Le diagramme à dessiner.
        """
        # Dessiner les arêtes (lignes bleues)
        for i, edge in enumerate(diagram.edges):
            x_coords = [edge.start.x, edge.end.x]
            y_coords = [edge.start.y, edge.end.y]
            label = 'Arêtes de Voronoï' if i == 0 else ''
            ax.plot(x_coords, y_coords, 'b-', linewidth=1.5, 
                   alpha=0.7, label=label)
        
        # Dessiner les sommets (points rouges)
        if diagram.vertices:
            vertices_x = [v.x for v in diagram.vertices]
            vertices_y = [v.y for v in diagram.vertices]
            ax.plot(vertices_x, vertices_y, 'ro', markersize=5, 
                   label='Sommets de Voronoï', zorder=5, alpha=0.8)
        
        # Dessiner les sites générateurs (points verts avec bordure)
        sites_x = [s.x for s in diagram.sites]
        sites_y = [s.y for s in diagram.sites]
        ax.plot(sites_x, sites_y, 'go', markersize=10, 
               label='Sites générateurs', zorder=10,
               markeredgecolor='darkgreen', markeredgewidth=2)
        
        # Annoter les sites avec leurs indices
        for i, site in enumerate(diagram.sites):
            ax.annotate(f'{i+1}', (site.x, site.y), 
                       textcoords="offset points", 
                       xytext=(0, 10), ha='center',
                       fontsize=8, color='darkgreen',
                       fontweight='bold')
        
        # Configurer les limites
        min_x, min_y, max_x, max_y = diagram.bounding_box
        range_x = max_x - min_x
        range_y = max_y - min_y
        margin = 0.1 * max(range_x, range_y)
        
        ax.set_xlim(min_x - margin, max_x + margin)
        ax.set_ylim(min_y - margin, max_y + margin)
        
        # Ajouter la légende
        ax.legend(loc='upper right', framealpha=0.95, 
                 edgecolor='black', fancybox=True, shadow=True)
        
        # Ajouter des statistiques dans un coin
        stats_text = (f'Sites : {len(diagram.sites)}\n'
                     f'Arêtes : {len(diagram.edges)}\n'
                     f'Sommets : {len(diagram.vertices)}')
        
        ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
               fontsize=9, verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))