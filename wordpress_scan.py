import subprocess
import sys

def run_wpscan(target):
    output_file = f'wpscan_{target}.json'
    try:
        # Exécution directe de la commande WPScan
        command = f"wpscan --url {target} --format json -o {output_file}"
        print(f"Exécution de WPScan avec la commande : {command}")
        
        # Utilisation de shell=True pour exécuter la commande exactement comme dans le terminal
        subprocess.run(command, shell=True, check=True)
        
        print(f"Le scan WPScan a été effectué, résultats enregistrés dans {output_file}")
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de WPScan : {e}")
        return None

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 wordpress_scan.py <target>")
        sys.exit(1)

    target = sys.argv[1]
    
    # Exécuter WPScan directement
    json_output = run_wpscan(target)

if __name__ == "__main__":
    main()
