import nmap
import csv
import sys

def scan_ports(target):
    """
    Effectue un scan Nmap sur la cible spécifiée et enregistre les résultats dans un fichier CSV.
    
    Args:
        target (str): L'adresse IP ou le nom DNS de la cible.
    """
    nm = nmap.PortScanner()
    
    # Lancer le scan Nmap avec les options -sS (SYN scan) et -sV (détection de version des services)
    nm.scan(target, '1-50000', arguments='-sS -sV')
    
    output_file = f'nmap_scan_{target}.csv'  # Nom du fichier CSV de sortie

    try:
        # Ouverture du fichier CSV pour écrire les résultats du scan
        with open(output_file, mode='w') as file:
            writer = csv.writer(file)
            # Écrire l'en-tête du CSV
            writer.writerow(['Port', 'State', 'Service', 'Version', 'Product', 'Extra Info', 'OS CPE'])

            # Parcours de chaque hôte scanné
            for host in nm.all_hosts():
                print(f'Scanning host: {host}')
                # Parcours des protocoles utilisés (comme TCP ou UDP)
                for proto in nm[host].all_protocols():
                    lport = nm[host][proto].keys()
                    # Parcours de chaque port scanné
                    for port in lport:
                        state = nm[host][proto][port]['state']  # État du port (open, closed, etc.)
                        service = nm[host][proto][port]['name']  # Service détecté (http, ssh, etc.)
                        version = nm[host][proto][port].get('version', 'N/A')  # Version du service
                        product = nm[host][proto][port].get('product', 'N/A')  # Produit associé au service
                        extra_info = nm[host][proto][port].get('extrainfo', 'N/A')  # Informations supplémentaires
                        os_cpe = nm[host][proto][port].get('cpe', 'N/A')  # CPE (Common Platform Enumeration)
                        
                        # Écrire les résultats dans le fichier CSV
                        writer.writerow([port, state, service, version, product, extra_info, os_cpe])
                        print(f'Port {port} is {state} ({service} - {version} - {product} - {extra_info} - {os_cpe})')

        print(f"Le fichier CSV a été créé avec succès : {output_file}")
    except Exception as e:
        print(f"Erreur lors de la création du fichier CSV : {e}")

if __name__ == "__main__":
    # Vérification du nombre d'arguments passés
    if len(sys.argv) != 2:
        print("Usage: python3 nmap_scan.py <target>")
        sys.exit(1)
    
    # Récupération de la cible depuis les arguments
    target = sys.argv[1]
    print(f"Lancement du scan Nmap pour la cible : {target}")
    
    # Lancement du scan
    scan_ports(target)
