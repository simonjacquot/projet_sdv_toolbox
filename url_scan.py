import csv
import sys
import subprocess
import re
from urllib.parse import unquote  # Pour décoder les URL encodées

# Fonction pour retirer les séquences ANSI
def remove_ansi_sequences(text):
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

def find_web_ports(csv_file):
    """Trouve les ports web (HTTP/HTTPS) dans le fichier CSV de Nmap."""
    web_ports = []
    try:
        with open(csv_file, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Sauter l'en-tête
            for row in reader:
                print(f"Lecture de la ligne du CSV : {row}")  # Debug: afficher chaque ligne lue
                port = row[0]
                service = row[2]
                if 'http' in service:  # Vérification des services HTTP/HTTPS
                    web_ports.append(port)
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier CSV Nmap : {e}")
    
    return web_ports

def scan_urls_with_gobuster(target, port):
    """Exécute Gobuster sur une URL et formate les résultats en CSV."""
    protocol = "https" if port == "443" else "http"
    url_base = f"{protocol}://{target}:{port}"
    output_file = f'gobuster_scan_{target}_{port}.csv'
    
    print(f"Exécution de Gobuster sur : {url_base}")
    
    try:
        # Commande Gobuster avec exclusion du code de statut 302
        gobuster_command = [
            'gobuster', 'dir',
            '-u', url_base,
            '-w', '/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt',
            '-q',
            '-b', '302'  # Exclure les redirections 302
        ]
        
        print(f"Commande Gobuster : {' '.join(gobuster_command)}")  # Debug: afficher la commande

        # Exécuter la commande et capturer la sortie
        result = subprocess.run(gobuster_command, capture_output=True, text=True, check=True)
        
        # Nettoyage des séquences ANSI
        clean_output = remove_ansi_sequences(result.stdout)
        
        # Analyse de la sortie de Gobuster
        lines = clean_output.splitlines()
        parsed_results = []

        # Utilisation d'une expression régulière pour extraire URL et code de statut HTTP
        pattern = re.compile(r"(\S+)\s+\(Status:\s+(\d+)\)\s+\[Size:\s+(\d+)\]")

        for line in lines:
            match = pattern.search(line)
            if match:
                url = unquote(match.group(1))  # Décodage de l'URL
                status_code = match.group(2)
                size = match.group(3)
                parsed_results.append([url, status_code, size])
        
        # Enregistrer les résultats parsés dans un fichier CSV
        with open(output_file, mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['URL', 'Status Code', 'Size'])  # En-têtes
            writer.writerows(parsed_results)  # Contenu
        
        print(f"Le fichier CSV des résultats Gobuster a été créé : {output_file}")
        
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de Gobuster : {e.stderr}")
    except Exception as e:
        print(f"Erreur lors de l'exécution de Gobuster : {e}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 url_scan.py <target>")
        sys.exit(1)
    
    target = sys.argv[1]
    nmap_csv = f'nmap_scan_{target}.csv'
    
    print(f"Analyse du fichier Nmap pour les ports web : {nmap_csv}")
    web_ports = find_web_ports(nmap_csv)
    
    if not web_ports:
        print("Aucun port web détecté.")
        sys.exit(0)
    
    print(f"Ports web détectés : {web_ports}")
    
    for port in web_ports:
        scan_urls_with_gobuster(target, port)

if __name__ == "__main__":
    main()
