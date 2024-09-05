import re
import subprocess
import csv
import sys
import os

# Dictionnaire de signatures d'applications pour identifier des technologies web spécifiques
APP_SIGNATURES = {
    'WordPress': ['wordpress', 'wp-content'],
    'Joomla': ['joomla', 'joomla!'],
    'Drupal': ['drupal', 'drupal.org'],
    'GLPI': ['glpi', 'teclib'],
    'Apache': ['apache', 'httpd'],
    'Nginx': ['nginx'],
    'IIS': ['microsoft-iis', 'asp.net'],
    'Magento': ['magento'],
    'phpBB': ['phpbb'],
    'MediaWiki': ['mediawiki'],
    'osCommerce': ['oscommerce'],
    'Liferay': ['liferay'],
    'OpenCart': ['opencart'],
    'Django': ['django'],
    'Ruby on Rails': ['rails', 'ruby on rails'],
    'Express': ['express', 'node.js'],
    'Vue.js': ['vue.js'],
    'Angular': ['angular.js', 'angular'],
    'React': ['react', 'reactjs'],
    'Spring': ['spring framework'],
    'Tomcat': ['tomcat', 'apache tomcat'],
    'Oracle': ['oracle'],
    'SAP': ['sap', 'sap netweaver'],
    'WebSphere': ['websphere'],
    'ColdFusion': ['coldfusion'],
    'Typo3': ['typo3'],
    'Moodle': ['moodle'],
    'Bitnami': ['bitnami'],
    'Zimbra': ['zimbra'],
    'Nextcloud': ['nextcloud'],
    'ownCloud': ['owncloud'],
    'Vbulletin': ['vbulletin'],
    'Ghost': ['ghost'],
    'Flask': ['flask'],
    'WildFly': ['wildfly'],
    'JBoss': ['jboss'],
    'WebLogic': ['weblogic'],
    'Grafana': ['grafana'],
    'Kibana': ['kibana'],
    'GitLab': ['gitlab'],
    'Jenkins': ['jenkins'],
    'Atlassian Confluence': ['confluence'],
    'Atlassian Jira': ['jira'],
    'SonarQube': ['sonarqube'],
    # Ajoutez d'autres signatures ici si nécessaire
}

# Fonction pour retirer les séquences ANSI de la sortie de WhatWeb
def remove_ansi_sequences(text):
    """Nettoie les séquences ANSI d'un texte pour un affichage propre."""
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

# Exécution de WhatWeb pour analyser une URL cible
def run_whatweb(target, port):
    """Exécute WhatWeb sur l'URL cible pour détecter les technologies en place."""
    url = f"http://{target}:{port}"
    try:
        # Exécute WhatWeb avec l'option -a 3 (analyse agressive)
        result = subprocess.run(['whatweb', '-a', '3', url], capture_output=True, text=True, check=True)
        cleaned_output = remove_ansi_sequences(result.stdout)
        return cleaned_output
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de WhatWeb : {e}")
        return None

# Détection de l'application web à partir de la sortie de WhatWeb
def detect_application(whatweb_output):
    """Identifie l'application web à partir des signatures connues."""
    for app, signatures in APP_SIGNATURES.items():
        for signature in signatures:
            if signature.lower() in whatweb_output.lower():
                return app
    return "Application non identifiée"

# Obtenir les ports à partir du fichier CSV généré par Nmap
def get_ports_from_csv(nmap_csv_file):
    """Extrait les ports du fichier CSV de Nmap."""
    ports = []
    with open(nmap_csv_file, 'r') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            ports.append(row['Port'])
    return ports

# Fonction principale qui gère l'analyse
def main():
    """Fonction principale du script."""
    if len(sys.argv) != 2:
        print("Usage: python3 whatweb.py <target>")
        sys.exit(1)

    target = sys.argv[1]
    nmap_csv_file = f"nmap_scan_{target}.csv"  # Fichier CSV de Nmap contenant les ports
    
    ports = get_ports_from_csv(nmap_csv_file)  # Extraction des ports à analyser
    
    # Fichiers de sortie : un fichier texte et un fichier CSV pour enregistrer les résultats
    with open(f"whatweb_results_{target}.txt", "w") as f_txt, open(f"whatweb_results_{target}.csv", "w", newline='') as f_csv:
        csv_writer = csv.writer(f_csv)
        csv_writer.writerow(["URL", "Application"])  # En-têtes du fichier CSV
        
        for port in ports:
            print(f"Exécution de WhatWeb sur http://{target}:{port}...")
            whatweb_output = run_whatweb(target, port)  # Exécution de WhatWeb pour chaque port
            
            if whatweb_output:
                app_detected = detect_application(whatweb_output)  # Détection de l'application web
                f_txt.write(f"http://{target}:{port} - {app_detected}\n")  # Écriture des résultats dans le fichier texte
                print(f"Application identifiée pour http://{target}:{port}: {app_detected}")
                
                # N'ajouter au CSV que si une application est identifiée
                if app_detected != "Application non identifiée":
                    csv_writer.writerow([f"http://{target}:{port}", app_detected])  # Écriture dans le fichier CSV
            else:
                f_txt.write(f"http://{target}:{port} - Analyse échouée\n")
                print(f"Analyse échouée pour http://{target}:{port}")
    
    print(f"Analyse terminée. Les résultats sont enregistrés dans whatweb_results_{target}.txt et whatweb_results_{target}.csv")

if __name__ == "__main__":
    main()
