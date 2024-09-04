import subprocess
import sys
import os
import csv

def run_wapiti_scan(target_url, output_file):
    """Exécute un scan Wapiti sur l'URL cible et sauvegarde le résultat dans un fichier JSON."""
    try:
        print(f"Exécution de Wapiti sur {target_url}")
        command = [
            'wapiti', '-u', target_url, '-f', 'json', '-o', output_file
        ]
        subprocess.run(command, check=True)
        print(f"Le scan Wapiti a été effectué, résultats enregistrés dans {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de Wapiti : {e}")
        sys.exit(1)

def get_urls_from_csv(csv_file, host):
    """Lit le CSV Nmap et retourne les URLs avec les préfixes appropriés."""
    urls = []
    try:
        print(f"Lecture du fichier CSV Nmap {csv_file}")
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                port = row.get('Port')
                service = row.get('Service')
                if port == '80':
                    urls.append(f'http://{host}')
                elif port == '443':
                    urls.append(f'https://{host}')
                else:
                    print(f"Port {port} avec service {service} ignoré.")
    except FileNotFoundError:
        print(f"Le fichier CSV {csv_file} n'a pas été trouvé.")
        sys.exit(1)
    return urls

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 vuln_scan.py <host>")
        sys.exit(1)

    host = sys.argv[1]
    nmap_csv_file = f"nmap_scan_{host.replace('/', '_').replace(':', '_')}.csv"

    # Obtenez les URLs à partir du CSV de Nmap
    urls = get_urls_from_csv(nmap_csv_file, host)

    if not urls:
        print("Aucune URL à scanner trouvée dans le fichier CSV.")
        sys.exit(1)

    # Exécuter Wapiti pour chaque URL
    for url in urls:
        url_safe = url.replace('http://', '').replace('https://', '').replace('/', '_').replace(':', '_')
        output_json = f"wapiti_scan_{url_safe}.json"
        
        run_wapiti_scan(url, output_json)

if __name__ == "__main__":
    main()
