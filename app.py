import subprocess
import os

def run_command(command, use_shell=False):
    """
    Exécute une commande shell, en utilisant ou non l'option `shell`.
    
    Args:
        command (str): La commande shell à exécuter.
        use_shell (bool): Si True, exécute la commande dans un sous-shell.
    """
    try:
        if use_shell:
            subprocess.run(command, shell=True, check=True, executable="/bin/bash")
        else:
            subprocess.run(command, check=True)
        print(f"Commande '{command}' exécutée avec succès.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de la commande '{command}': {e}")

def run_script_in_venv(venv_path, script_name, *args):
    """
    Exécute un script Python dans l'environnement virtuel (venv).
    
    Args:
        venv_path (str): Chemin du dossier de l'environnement virtuel.
        script_name (str): Nom du script Python à exécuter.
        *args: Arguments supplémentaires à passer au script Python.
    """
    # Localisation de l'exécutable Python dans le venv
    python_venv = os.path.join(venv_path, "bin", "python3.11")
    command = [python_venv, script_name] + list(args)
    
    try:
        # Exécution du script dans le venv
        subprocess.run(command, check=True)
        print(f"Le script {script_name} a été exécuté avec succès.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de {script_name} : {e}")

def main():
    """
    Fonction principale qui exécute toutes les étapes nécessaires à l'installation des dépendances,
    à la configuration de l'environnement virtuel et à l'exécution des différents scripts d'analyse.
    """
    # Demander à l'utilisateur l'adresse IP ou le nom de domaine cible
    target = input("Veuillez entrer l'adresse IP ou le nom DNS de la cible: ")

    # Commande d'installation des outils et création de l'environnement virtuel (venv)
    setup_commands = f'''
    apt update &&
    apt install -y python3.11 python3.11-venv python3.11-dev &&
    apt-get install -y gobuster wpscan python3-nmap &&
    python3.11 -m venv venv &&
    source venv/bin/activate &&
    pip install --upgrade pip setuptools &&
    pip install -r requirements.txt
    '''
    
    # Exécuter les commandes pour installer les dépendances et créer le venv
    run_command(setup_commands, use_shell=True)

    # Définir le chemin absolu vers le venv
    venv_path = os.path.abspath("venv")

    # Exécuter les scripts d'analyse dans l'ordre
    run_script_in_venv(venv_path, 'nmap_scan.py', target)  # Scan des ports avec Nmap
    run_script_in_venv(venv_path, 'whatweb.py', target)     # Analyse des technologies web avec WhatWeb
    run_script_in_venv(venv_path, 'url_scan.py', target)    # Scan des URLs trouvées
    run_script_in_venv(venv_path, 'wordpress_scan.py', target)  # Analyse des vulnérabilités WordPress

    # Générer des fichiers résumés à partir des résultats de WPScan
    wpscan_json = f"wpscan_{target.replace('/', '_').replace(':', '_')}.json"
    summary_csv = f"wpscan_{target.replace('/', '_').replace(':', '_')}_summary.csv"
    run_script_in_venv(venv_path, 'summarize_wpscan.py', wpscan_json, summary_csv)

    # Scanner les vulnérabilités avec Wapiti
    run_script_in_venv(venv_path, 'vuln_scan.py', target)

    # Résumer les résultats de Wapiti
    wapiti_json = f"wapiti_scan_{target.replace('/', '_').replace(':', '_')}.json"
    wapiti_summary_csv = f"wapiti_scan_{target.replace('/', '_').replace(':', '_')}_summary.csv"
    run_script_in_venv(venv_path, 'summarize_wapiti.py', wapiti_json, wapiti_summary_csv)

    # Démarrer Metasploit RPC pour exploiter les CVE/CWE
    run_script_in_venv(venv_path, 'setup_metasploit_rpc.py')

    # Extraire les CVE/CWE et lancer les exploits
    cve_cwe_csv = f"cve_cwe_extraction_{target.replace('/', '_').replace(':', '_')}.csv"
    run_script_in_venv(venv_path, 'extract_cve_cwe.py', wapiti_json, cve_cwe_csv)

    # Si des CVE/CWE ont été extraites, tenter d'exploiter les vulnérabilités
    if os.path.exists(cve_cwe_csv):
        output_results_csv = f"exploit_results_{target.replace('/', '_').replace(':', '_')}.csv"
        run_script_in_venv(venv_path, 'exploit_cve_cwe.py', cve_cwe_csv, target, output_results_csv)
    else:
        print(f"Le fichier {cve_cwe_csv} n'existe pas. Aucune CVE/CWE n'a été trouvée ou extraite.")

    # Exécuter d'autres scripts pour exploitation et tests complémentaires
    run_script_in_venv(venv_path, 'exploit_appli.py', target)
    run_script_in_venv(venv_path, 'brute_force.py', target)  # Brute force sur les ports ouverts
    run_script_in_venv(venv_path, 'resume_results.py', target)  # Résumé des résultats
    run_script_in_venv(venv_path, 'move.py', target)  # Déplacer les fichiers dans le dossier cible
    run_script_in_venv(venv_path, 'serveur_web.py', target)  # Lancer le serveur web pour afficher les résultats

if __name__ == "__main__":
    main()
