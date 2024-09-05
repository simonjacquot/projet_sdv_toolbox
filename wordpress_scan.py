import subprocess
import sys

def run_wpscan(target):
    """Exécute un scan WPScan sur l'URL cible et enregistre le résultat dans un fichier JSON."""
    output_file = f'wpscan_{target}.json'  # Définir le nom de sortie du fichier JSON
    try:
        # Commande WPScan à exécuter avec format JSON
        command = f"wpscan --url {target} --format json -o {output_file}"
        print(f"Exécution de WPScan avec la commande : {command}")
        
        # Utilisation de shell=True pour exécuter la commande exactement comme dans le terminal
        subprocess.run(command, shell=True, check=True)  # Exécute la commande avec WPScan
        
        print(f"Le scan WPScan a été effectué, résultats enregistrés dans {output_file}")
        return output_file  # Renvoie le chemin du fichier de sortie
    except subprocess.CalledProcessError as e:
        # En cas d'échec d'exécution de WPScan, afficher l'erreur
        print(f"Erreur lors de l'exécution de WPScan : {e}")
        return None

def main():
    """Fonction principale qui récupère la cible et lance le scan WPScan."""
    if len(sys.argv) != 2:
        print("Usage: python3 wordpress_scan.py <target>")  # Message d'utilisation en cas de paramètres manquants
        sys.exit(1)

    target = sys.argv[1]  # Récupérer la cible passée en paramètre
    
    # Exécuter WPScan directement sur la cible
    json_output = run_wpscan(target)

if __name__ == "__main__":
    main()
