import re
import subprocess
import csv
import sys
import os

# Signatures d'applications
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
    # Ajoutez d'autres signatures ici
}

def remove_ansi_sequences(text):
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

def run_whatweb(target, port):
    url = f"http://{target}:{port}"
    try:
        result = subprocess.run(['whatweb', '-a', '3', url], capture_output=True, text=True, check=True)
        cleaned_output = remove_ansi_sequences(result.stdout)
        return cleaned_output
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de WhatWeb : {e}")
        return None

def detect_application(whatweb_output):
    for app, signatures in APP_SIGNATURES.items():
        for signature in signatures:
            if signature.lower() in whatweb_output.lower():
                return app
    return "Application non identifiée"

def get_ports_from_csv(nmap_csv_file):
    ports = []
    with open(nmap_csv_file, 'r') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            ports.append(row['Port'])
    return ports

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 whatweb.py <target>")
        sys.exit(1)

    target = sys.argv[1]
    nmap_csv_file = f"nmap_scan_{target}.csv"
    
    ports = get_ports_from_csv(nmap_csv_file)
    
    with open(f"whatweb_results_{target}.txt", "w") as f_txt, open(f"whatweb_results_{target}.csv", "w", newline='') as f_csv:
        csv_writer = csv.writer(f_csv)
        csv_writer.writerow(["URL", "Application"])
        
        for port in ports:
            print(f"Exécution de WhatWeb sur http://{target}:{port}...")
            whatweb_output = run_whatweb(target, port)
            if whatweb_output:
                app_detected = detect_application(whatweb_output)
                f_txt.write(f"http://{target}:{port} - {app_detected}\n")
                print(f"Application identifiée pour http://{target}:{port}: {app_detected}")
                
                # N'ajouter au CSV que si une application est identifiée
                if app_detected != "Application non identifiée":
                    csv_writer.writerow([f"http://{target}:{port}", app_detected])
            else:
                f_txt.write(f"http://{target}:{port} - Analyse échouée\n")
                print(f"Analyse échouée pour http://{target}:{port}")
    
    print(f"Analyse terminée. Les résultats sont enregistrés dans whatweb_results_{target}.txt et whatweb_results_{target}.csv")

if __name__ == "__main__":
    main()
