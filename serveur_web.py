import pandas as pd
import os
import sys
import webbrowser
from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)

# Dictionnaire pour associer les titres aux fichiers CSV avec leurs noms compréhensibles
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
    """
    Extrait et résume les résultats d'exploitation du fichier CSV des exploits.
    
    Args:
        file_path (str): Chemin vers le fichier CSV des résultats d'exploitation.
    
    Returns:
        tuple: Un dictionnaire avec le nombre d'exploits réussis et échoués, et le DataFrame complet des résultats.
    """
    df = pd.read_csv(file_path)
    success_count = df[df['Résultat'] == 'réussi'].shape[0]  # Nombre d'exploits réussis
    fail_count = df[df['Résultat'] == 'échoué'].shape[0]  # Nombre d'exploits échoués
    return {"success": success_count, "fail": fail_count}, df

@app.route('/')
def index():
    """
    Charge et affiche les résultats des différents scans sous forme de tableaux.
    
    Returns:
        Le rendu HTML de la page principale avec les résultats organisés.
    """
    target = sys.argv[1]  # Récupère la cible depuis les arguments de ligne de commande
    current_date = datetime.today().strftime('%Y-%m-%d')  # Obtenir la date actuelle
    target_folder_name = f"{target.replace('/', '_').replace(':', '_')}_{current_date}"
    results_folder = os.path.join("results", target_folder_name)  # Chemin vers le dossier des résultats
    
    csv_files = {}  # Stockage des fichiers CSV chargés
    summary_data = {}  # Résumé des résultats
    exploit_summary = {}  # Résumé des exploits (réussi/échoué)
    exploit_results = None  # DataFrame des résultats d'exploit
    
    # Parcourir les fichiers CSV dans le dossier des résultats
    for file_name in os.listdir(results_folder):
        if file_name.endswith('.csv'):  # Vérifie si le fichier est un CSV
            file_path = os.path.join(results_folder, file_name)
            try:
                df = pd.read_csv(file_path)
                if not df.empty:
                    # Identifier le type de fichier CSV à partir de son nom
                    for key, title in FILE_TITLES.items():
                        if key in file_name:
                            if "exploit_result" in file_name:  # Résumé des exploits
                                exploit_summary, exploit_results = extract_exploit_summary(file_path)
                            elif "summary_results" in file_name:  # Résumé global
                                summary_data = df.to_dict(orient='records')[0]  # Convertir le CSV en dictionnaire
                                print(f"Résumé des résultats chargé : {summary_data}")
                            else:
                                csv_files[title] = df  # Ajouter le fichier CSV sous son titre
                            break
            except pd.errors.EmptyDataError:
                print(f"Le fichier {file_name} est vide et ne sera pas chargé.")
            except Exception as e:
                print(f"Erreur lors de la lecture du fichier {file_name}: {e}")

    # Trier les fichiers CSV dans l'ordre défini par FILE_TITLES
    ordered_csv_files = {title: csv_files[title] for title in FILE_TITLES.values() if title in csv_files}

    # Retourne le rendu HTML avec les données des CSV et des résumés
    return render_template('index.html', csv_files=ordered_csv_files, summary_data=summary_data, exploit_summary=exploit_summary, exploit_results=exploit_results, current_date=current_date)

if __name__ == '__main__':
    webbrowser.open("http://127.0.0.1:5000")  # Ouvre automatiquement le navigateur à l'adresse locale
    app.run(debug=True)  # Démarre le serveur Flask en mode débogage
