import csv
import os
import sys
import pandas as pd

def count_rows_in_csv(file_path):
    """
    Compte le nombre de lignes (résultats) dans un fichier CSV en excluant l'en-tête.
    
    Args:
        file_path (str): Chemin vers le fichier CSV.
    
    Returns:
        int: Nombre de lignes dans le fichier CSV.
    """
    try:
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            row_count = sum(1 for row in reader) - 1  # Soustraire 1 pour ignorer l'en-tête
            return row_count
    except FileNotFoundError:
        print(f"Fichier non trouvé : {file_path}")
        return 0

def count_successful_brute_force(brute_force_csv_file):
    """
    Compte le nombre de tentatives de brute force réussies dans un fichier CSV.
    
    Args:
        brute_force_csv_file (str): Chemin vers le fichier CSV contenant les résultats du brute force.
    
    Returns:
        int: Nombre de tentatives réussies.
    """
    try:
        df = pd.read_csv(brute_force_csv_file)
        # Vérifier si le fichier est vide ou contient l'information d'échec
        if df.empty or "Échec du brute force" in df.to_string():
            return 0
        return len(df)  # Nombre de tentatives réussies
    except FileNotFoundError:
        print(f"Fichier non trouvé : {brute_force_csv_file}")
        return 0

def generate_summary_csv(target):
    """
    Génère un fichier CSV résumant le nombre de vulnérabilités, de ports ouverts et de brute force réussis.
    
    Args:
        target (str): Cible de la génération du résumé.
    """
    # Générer les noms de fichiers en fonction de la cible
    cve_cwe_csv = f"cve_cwe_extraction_{target.replace('/', '_').replace(':', '_')}.csv"
    nmap_csv = f"nmap_scan_{target.replace('/', '_').replace(':', '_')}.csv"
    brute_force_csv = f"brute_force_results_{target.replace('/', '_').replace(':', '_')}.csv"
    output_csv = f"summary_results_{target.replace('/', '_').replace(':', '_')}.csv"

    # Compter les vulnérabilités CVE/CWE
    print(f"Vérification du fichier : {cve_cwe_csv}")
    cve_cwe_count = count_rows_in_csv(cve_cwe_csv)
    print(f"Nombre de vulnérabilités : {cve_cwe_count}")

    # Compter les ports ouverts
    print(f"Vérification du fichier : {nmap_csv}")
    ports_count = count_rows_in_csv(nmap_csv)
    print(f"Nombre de ports ouverts : {ports_count}")

    # Compter les succès de brute force
    print(f"Vérification du fichier : {brute_force_csv}")
    brute_force_count = count_successful_brute_force(brute_force_csv)
    print(f"Nombre de brute force réussis : {brute_force_count}")

    # Écrire les résultats dans un fichier CSV
    with open(output_csv, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["cve_cwe", "ports", "bruteforce"])  # En-têtes
        writer.writerow([cve_cwe_count, ports_count, brute_force_count])  # Résultats

    print(f"Résumé généré avec succès dans {output_csv}")

def main(target):
    """
    Fonction principale pour générer le résumé des résultats pour une cible donnée.
    
    Args:
        target (str): L'adresse IP ou nom DNS de la cible.
    """
    print(f"Génération du résumé pour la cible : {target}")
    generate_summary_csv(target)

if __name__ == "__main__":
    # Vérification du nombre d'arguments passés
    if len(sys.argv) < 2:
        print("Usage: python resume_results.py <target>")
        sys.exit(1)
    
    # Appel de la fonction principale avec la cible spécifiée
    main(sys.argv[1])
