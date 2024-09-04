import csv
import os
import sys
import pandas as pd

def count_rows_in_csv(file_path):
    """Compte le nombre de lignes dans un fichier CSV."""
    try:
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            row_count = sum(1 for row in reader) - 1  # Soustraire 1 pour ignorer l'en-tête
            return row_count
    except FileNotFoundError:
        print(f"Fichier non trouvé : {file_path}")
        return 0

def count_successful_brute_force(brute_force_csv_file):
    """Compter le nombre de tentatives de brute force réussies."""
    try:
        df = pd.read_csv(brute_force_csv_file)
        if df.empty or "Échec du brute force" in df.to_string():
            return 0
        return len(df)
    except FileNotFoundError:
        print(f"Fichier non trouvé : {brute_force_csv_file}")
        return 0

def generate_summary_csv(target):
    """Génère un résumé des résultats sous forme de CSV."""
    cve_cwe_csv = f"cve_cwe_extraction_{target.replace('/', '_').replace(':', '_')}.csv"
    nmap_csv = f"nmap_scan_{target.replace('/', '_').replace(':', '_')}.csv"
    brute_force_csv = f"brute_force_results_{target.replace('/', '_').replace(':', '_')}.csv"
    output_csv = f"summary_results_{target.replace('/', '_').replace(':', '_')}.csv"

    print(f"Vérification du fichier : {cve_cwe_csv}")
    cve_cwe_count = count_rows_in_csv(cve_cwe_csv)
    print(f"Nombre de vulnérabilités : {cve_cwe_count}")

    print(f"Vérification du fichier : {nmap_csv}")
    ports_count = count_rows_in_csv(nmap_csv)
    print(f"Nombre de ports ouverts : {ports_count}")

    print(f"Vérification du fichier : {brute_force_csv}")
    brute_force_count = count_successful_brute_force(brute_force_csv)
    print(f"Nombre de brute force réussis : {brute_force_count}")

    # Écrire les résultats dans un fichier CSV
    with open(output_csv, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["cve_cwe", "ports", "bruteforce"])
        writer.writerow([cve_cwe_count, ports_count, brute_force_count])

    print(f"Résumé généré avec succès dans {output_csv}")

def main(target):
    print(f"Génération du résumé pour la cible : {target}")
    generate_summary_csv(target)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python resume_results.py <target>")
        sys.exit(1)
    
    main(sys.argv[1])
