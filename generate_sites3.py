import json
import random
import argparse

def generate_sites(n: int, x_max: float = 100.0, y_max: float = 100.0, output: str = "liste_de_sites.json"):
    sites = [{str(round(random.uniform(0, x_max), 1)): str(round(random.uniform(0, y_max), 1))} for _ in range(n)]
    with open(output, "w") as f:
        json.dump(sites, f, indent=2)
    print(f"{n} points écrits dans '{output}'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Génère un fichier JSON de sites aléatoires.")
    parser.add_argument("n", type=int, help="Nombre de points à générer")
    parser.add_argument("--x_max", type=float, default=100.0, help="Valeur max pour x (défaut: 100)")
    parser.add_argument("--y_max", type=float, default=100.0, help="Valeur max pour y (défaut: 100)")
    parser.add_argument("--output", type=str, default="liste_de_sites.json", help="Fichier de sortie")
    args = parser.parse_args()

    generate_sites(args.n, args.x_max, args.y_max, args.output)
