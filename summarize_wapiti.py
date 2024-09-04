import json
import csv
import sys

def clean_http_request(http_request):
    """Nettoie la requête HTTP en retirant les parties non nécessaires."""
    lines = http_request.splitlines()
    # Retirer les lignes spécifiques
    cleaned_lines = []
    for line in lines:
        if not line.startswith(("GET /", "POST /", "Host:", "Connection:", "User-Agent:")):
            cleaned_lines.append(line)
    return "\n".join(cleaned_lines)

def extract_vulnerabilities(data):
    """Extrait les vulnérabilités du fichier JSON."""
    vulnerabilities = []

    for vuln_category, vuln_list in data.get('vulnerabilities', {}).items():
        for vuln in vuln_list:
            cleaned_http_request = clean_http_request(vuln.get("http_request", ""))
            vulnerabilities.append({
                "Category": vuln_category,
                "Module": vuln.get("module", ""),
                "Path": vuln.get("path", ""),
                "Parameter": vuln.get("parameter", ""),
                "Info": vuln.get("info", ""),
                "WSTG Reference": ", ".join(vuln.get("wstg", [])),
                "HTTP Request": cleaned_http_request
            })

    return vulnerabilities

def write_csv(vulnerabilities, output_csv):
    """Écrit les vulnérabilités dans un fichier CSV."""
    try:
        with open(output_csv, mode='w', newline='') as csvfile:
            fieldnames = ["Category", "Module", "Path", "Parameter", "Info", "WSTG Reference", "HTTP Request"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for vuln in vulnerabilities:
                writer.writerow(vuln)

        print(f"Les résultats ont été exportés vers {output_csv}")
    except Exception as e:
        print(f"Erreur lors de l'écriture du fichier CSV : {e}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 summarize_wapiti.py <input_json_file> <output_csv_file>")
        sys.exit(1)

    input_json = sys.argv[1]
    output_csv = sys.argv[2]

    try:
        with open(input_json, 'r') as json_file:
            data = json.load(json_file)
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier JSON : {e}")
        sys.exit(1)

    vulnerabilities = extract_vulnerabilities(data)
    write_csv(vulnerabilities, output_csv)

if __name__ == "__main__":
    main()
