import pandas as pd
import os
import sys
import webbrowser
from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)

# Dictionnaire pour associer les titres aux fichiers CSV
FILE_TITLES = {
    "nmap_scan": "1- Ports ouverts",
    "whatweb_results": "2- Résultats WhatWeb",
    "gobuster_scan": "3- Scan Gobuster",
    "brute_force_results": "4- Résultats du Brute Force",
    "wapiti_scan": "5- Scan Wapiti",
    "cve_cwe_extraction": "6- Vulnérabilités (CVE/CWE)",
    "metasploit_app": "7- Résultats Metasploit",
    "exploit_results": "8- Exploitation CVE / CWE",
    "wpscan": "9- Résultats WPScan",
    "summary_results": "Résumé des résultats"
}

def extract_exploit_summary(file_path):
    """Extrait les réussis et échecs du fichier exploit_result"""
    df = pd.read_csv(file_path)
    success_count = df[df['Résultat'] == 'réussi'].shape[0]
    fail_count = df[df['Résultat'] == 'échoué'].shape[0]
    return {"success": success_count, "fail": fail_count}, df

@app.route('/')
def index():
    target = sys.argv[1]
    current_date = datetime.today().strftime('%Y-%m-%d')  # Date actuelle au format année-mois-jour
    target_folder_name = f"{target.replace('/', '_').replace(':', '_')}_{current_date}"
    results_folder = os.path.join("results", target_folder_name)
    
    csv_files = {}
    summary_data = {}
    exploit_summary = {}
    exploit_results = None

    # Charger les fichiers CSV
    for file_name in os.listdir(results_folder):
        if file_name.endswith('.csv'):
            file_path = os.path.join(results_folder, file_name)
            try:
                df = pd.read_csv(file_path)
                if not df.empty:
                    for key, title in FILE_TITLES.items():
                        if key in file_name:
                            if "exploit_result" in file_name:
                                exploit_summary, exploit_results = extract_exploit_summary(file_path)
                            elif "summary_results" in file_name:
                                summary_data = df.to_dict(orient='records')[0]  # Charger les données du résumé
                                print(f"Résumé des résultats chargé : {summary_data}")
                            else:
                                csv_files[title] = df
                            break
            except pd.errors.EmptyDataError:
                print(f"Le fichier {file_name} est vide et ne sera pas chargé.")
            except Exception as e:
                print(f"Erreur lors de la lecture du fichier {file_name}: {e}")

    # Trier csv_files en fonction de l'ordre de FILE_TITLES
    ordered_csv_files = {title: csv_files[title] for title in FILE_TITLES.values() if title in csv_files}

    return render_template('index.html', csv_files=ordered_csv_files, summary_data=summary_data, exploit_summary=exploit_summary, exploit_results=exploit_results, current_date=current_date)

if __name__ == '__main__':
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=True)
