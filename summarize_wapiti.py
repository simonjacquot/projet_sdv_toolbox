import json
import csv
import sys

def clean_http_request(http_request):
    """
    Nettoie une requête HTTP en supprimant les en-têtes non pertinents.
    
    Args:
        http_request (str): La requête HTTP brute à nettoyer.
    
    Returns:
        str: La requête nettoyée, prête à être incluse dans le rapport.
    """
    lines = http_request.splitlines()
    cleaned_lines = []
    # Filtrer les en-têtes spécifiques que nous ne voulons pas dans le rapport
    for line in lines:
        if not line.startswith(("GET /", "POST /", "Host:", "Connection:", "User-Agent:")):
            cleaned_lines.append(line)
    return "\n".join(cleaned_lines)

def extract_vulnerabilities(data):
    """
    Extrait les vulnérabilités à partir des données JSON de Wapiti.
    
    Args:
        data (dict): Les données JSON issues du scan Wapiti.
    
    Returns:
        list: Une liste de dictionnaires contenant les vulnérabilités formatées pour le CSV.
    """
    vulnerabilities = []

    # Parcourir les catégories de vulnérabilités
    for vuln_category, vuln_list in data.get('vulnerabilities', {}).items():
        for vuln in vuln_list:
            cleaned_http_request = clean_http_request(vuln.get("http_request", ""))
            vulnerabilities.append({
                "Category": vuln_category,
                "Module": vuln.get("module", ""),  # Module concerné
                "Path": vuln.get("path", ""),  # Chemin où la vulnérabilité a été trouvée
                "Parameter": vuln.get("parameter", ""),  # Paramètre affecté par la vulnérabilité
                "Info": vuln.get("info", ""),  # Description de la vulnérabilité
                "WSTG Reference": ", ".join(vuln.get("wstg", [])),  # Références à la norme WSTG
                "HTTP Request": cleaned_http_request  # Requête HTTP nettoyée
            })

    return vulnerabilities

def write_csv(vulnerabilities, output_csv):
    """
    Écrit les vulnérabilités extraites dans un fichier CSV.
    
    Args:
        vulnerabilities (list): La liste des vulnérabilités formatées pour le CSV.
        output_csv (str): Le chemin du fichier CSV où les vulnérabilités seront enregistrées.
    """
    try:
        with open(output_csv, mode='w', newline='') as csvfile:
            fieldnames = ["Category", "Module", "Path", "Parameter", "Info", "WSTG Reference", "HTTP Request"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()  # Écrire l'en-tête du CSV
            for vuln in vulnerabilities:
                writer.writerow(vuln)  # Écrire chaque vulnérabilité dans le CSV

        print(f"Les résultats ont été exportés vers {output_csv}")
    except Exception as e:
        print(f"Erreur lors de l'écriture du fichier CSV : {e}")

def main():
    """
    Fonction principale du script. Elle gère la lecture des arguments et l'exécution du pipeline de traitement.
    """
    if len(sys.argv) != 3:
        print("Usage: python3 summarize_wapiti.py <input_json_file> <output_csv_file>")
        sys.exit(1)

    input_json = sys.argv[1]  # Fichier d'entrée JSON
    output_csv = sys.argv[2]  # Fichier de sortie CSV

    try:
        # Charger les données JSON depuis le fichier
        with open(input_json, 'r') as json_file:
            data = json.load(json_file)
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier JSON : {e}")
        sys.exit(1)

    # Extraire les vulnérabilités et écrire le rapport CSV
    vulnerabilities = extract_vulnerabilities(data)
    write_csv(vulnerabilities, output_csv)

if __name__ == "__main__":
    main()
