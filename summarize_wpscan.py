import json
import csv
import sys

def summarize_wpscan(json_file, output_csv):
    """
    Résume les résultats d'un fichier JSON produit par WPScan et les écrit dans un fichier CSV.

    Args:
        json_file (str): Le chemin vers le fichier JSON produit par WPScan.
        output_csv (str): Le chemin du fichier CSV de sortie où les résultats seront écrits.
    """
    try:
        # Lecture du fichier JSON
        with open(json_file, 'r') as file:
            data = json.load(file)
        
        # Ouverture du fichier CSV pour écrire les résultats
        with open(output_csv, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            # Écriture de l'en-tête du fichier CSV
            writer.writerow(['Category', 'Item', 'Details', 'Additional Info'])

            # Analyse des 'interesting_findings' (Découvertes intéressantes)
            if "interesting_findings" in data:
                for finding in data['interesting_findings']:
                    writer.writerow([
                        'Interesting Finding',  # Catégorie
                        finding.get('to_s', 'N/A'),  # Résumé de la découverte
                        finding.get('url', 'N/A'),  # URL associée
                        ', '.join(finding.get('interesting_entries', []))  # Entrées supplémentaires
                    ])

            # Analyse du thème principal (s'il y a un thème principal utilisé)
            if "main_theme" in data:
                theme = data['main_theme']
                writer.writerow([
                    'Theme',  # Catégorie
                    theme.get('style_name', 'N/A'),  # Nom du thème
                    theme.get('location', 'N/A'),  # Emplacement du thème
                    theme.get('version', {}).get('number', 'N/A')  # Version du thème
                ])

            # Analyse des plugins trouvés
            if "plugins" in data:
                for plugin_name, plugin_data in data['plugins'].items():
                    writer.writerow([
                        'Plugin',  # Catégorie
                        plugin_data.get('slug', plugin_name),  # Nom du plugin
                        plugin_data.get('location', 'N/A'),  # Emplacement du plugin
                        plugin_data.get('version', {}).get('number', 'N/A')  # Version du plugin
                    ])

            # Vérification des erreurs de l'API de vulnérabilité
            if "vuln_api" in data and "error" in data["vuln_api"]:
                writer.writerow([
                    'Vulnerability API',  # Catégorie
                    'Error',  # Erreur
                    data["vuln_api"]["error"],  # Message d'erreur
                    'N/A'  # Informations supplémentaires non disponibles
                ])

        print(f"Le résumé des résultats de WPScan a été exporté vers {output_csv}")

    except Exception as e:
        print(f"Erreur lors de la création du résumé CSV : {e}")

def main():
    """
    Fonction principale du script, responsable de l'analyse des arguments et de l'exécution de la fonction de résumé.
    """
    if len(sys.argv) != 3:
        print("Usage: python3 summarize_wpscan.py <wpscan_json_file> <output_csv_file>")
        sys.exit(1)

    json_file = sys.argv[1]  # Fichier JSON de WPScan
    output_csv = sys.argv[2]  # Fichier CSV de sortie

    # Appel de la fonction de résumé
    summarize_wpscan(json_file, output_csv)

if __name__ == "__main__":
    main()
