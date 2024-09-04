import json
import re
import csv
import sys

def extract_cve_cwe(data):
    """Extraire les CVE et CWE à partir des vulnérabilités."""
    cve_cwe_list = []

    # Fonction pour extraire les CVE et CWE d'une chaîne de texte
    def extract_refs(text):
        cve_matches = re.findall(r'CVE-\d{4}-\d{4,7}', text)
        cwe_matches = re.findall(r'CWE-\d{1,4}', text)
        for cve in cve_matches:
            cve_cwe_list.append(cve.replace('CVE-', 'CVE '))
        for cwe in cwe_matches:
            cve_cwe_list.append(cwe.replace('CWE-', 'CWE '))

    # Parcourir chaque classification de vulnérabilité
    for vuln_type, details in data['classifications'].items():
        print(f"Analyse de la vulnérabilité {vuln_type}")
        # Vérifier s'il y a des références CVE ou CWE
        if 'ref' in details:
            for ref_id, url in details['ref'].items():
                extract_refs(ref_id)

    return cve_cwe_list

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 extract_cve_cwe.py <json_file> <output_csv_file>")
        sys.exit(1)

    json_file = sys.argv[1]
    csv_file = sys.argv[2]

    # Charger le fichier JSON et extraire les CVE et CWE
    with open(json_file, 'r') as file:
        data = json.load(file)
        cve_cwe_list = extract_cve_cwe(data)

    # Sauvegarder les CVE et CWE extraites dans un fichier CSV
    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Type', 'ID'])  # En-têtes du fichier CSV
        for item in cve_cwe_list:
            writer.writerow(item.split())

    print(f"Extraction des CVE et CWE terminée. Résultats sauvegardés dans {csv_file}.")

if __name__ == "__main__":
    main()
