import json
import re
import csv
import sys

# Fonction pour extraire les CVE et CWE à partir des vulnérabilités
def extract_cve_cwe(data):
    """
    Extrait les CVE et CWE à partir des données de vulnérabilités JSON.

    Args:
        data (dict): Données JSON contenant les classifications de vulnérabilité.
    
    Returns:
        list: Liste des CVE et CWE extraits.
    """
    cve_cwe_list = []

    # Fonction locale pour extraire les CVE et CWE d'une chaîne de texte
    def extract_refs(text):
        """
        Recherche des CVE et CWE dans le texte donné.

        Args:
            text (str): Chaîne de texte à analyser.
        """
        # Recherche des CVE (ex: CVE-2021-1234) et CWE (ex: CWE-79) dans le texte
        cve_matches = re.findall(r'CVE-\d{4}-\d{4,7}', text)
        cwe_matches = re.findall(r'CWE-\d{1,4}', text)

        # Ajout des CVE et CWE dans la liste sous une forme standardisée
        for cve in cve_matches:
            cve_cwe_list.append(cve.replace('CVE-', 'CVE '))
        for cwe in cwe_matches:
            cve_cwe_list.append(cwe.replace('CWE-', 'CWE '))

    # Parcours des classifications de vulnérabilités dans le JSON
    for vuln_type, details in data['classifications'].items():
        print(f"Analyse de la vulnérabilité {vuln_type}")
        
        # Si des références CVE ou CWE sont présentes, on les extrait
        if 'ref' in details:
            for ref_id, url in details['ref'].items():
                extract_refs(ref_id)

    return cve_cwe_list

# Fonction principale du script
def main():
    """
    Fonction principale qui gère l'extraction des CVE et CWE à partir d'un fichier JSON
    et les enregistre dans un fichier CSV.
    """
    if len(sys.argv) != 3:
        print("Usage: python3 extract_cve_cwe.py <json_file> <output_csv_file>")
        sys.exit(1)

    json_file = sys.argv[1]  # Fichier JSON contenant les vulnérabilités
    csv_file = sys.argv[2]  # Fichier CSV de sortie pour sauvegarder les CVE/CWE extraits

    # Chargement du fichier JSON et extraction des CVE et CWE
    with open(json_file, 'r') as file:
        data = json.load(file)  # Charger les données JSON
        cve_cwe_list = extract_cve_cwe(data)  # Extraire les CVE et CWE

    # Sauvegarder les CVE et CWE extraits dans le fichier CSV
    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Type', 'ID'])  # En-têtes du fichier CSV (Type et ID)
        
        # Écriture de chaque CVE/CWE sous la forme "Type ID"
        for item in cve_cwe_list:
            writer.writerow(item.split())

    print(f"Extraction des CVE et CWE terminée. Résultats sauvegardés dans {csv_file}.")

if __name__ == "__main__":
    main()
