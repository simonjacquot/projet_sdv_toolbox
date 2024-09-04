import subprocess
import os

def run_command(command, use_shell=False):
    """Exécute une commande shell."""
    try:
        if use_shell:
            subprocess.run(command, shell=True, check=True, executable="/bin/bash")
        else:
            subprocess.run(command, check=True)
        print(f"Commande '{command}' exécutée avec succès.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de la commande '{command}': {e}")

def run_script_in_venv(venv_path, script_name, *args):
    """Exécute un script dans le venv."""
    python_venv = os.path.join(venv_path, "bin", "python3")
    command = [python_venv, script_name] + list(args)
    try:
        subprocess.run(command, check=True)
        print(f"Le script {script_name} a été exécuté avec succès.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de {script_name} : {e}")

def main():
    target = input("Veuillez entrer l'adresse IP ou le nom DNS de la cible: ")

    # Commandes à exécuter dans un seul sous-shell pour installer les outils et créer le venv
    setup_commands = f'''
    apt install -y python3.11-venv &&
    apt-get install -y gobuster wpscan python3-nmap &&
    python3 -m venv venv &&
    source venv/bin/activate &&
    pip install --upgrade pip setuptools &&
    pip install -r requirements.txt
    '''
    
    # Exécuter les commandes pour configurer l'environnement
    run_command(setup_commands, use_shell=True)

    venv_path = os.path.abspath("venv")  # Chemin absolu vers le venv

    # Exécuter les scripts après l'installation des dépendances
    run_script_in_venv(venv_path, 'nmap_scan.py', target)
    run_script_in_venv(venv_path, 'whatweb.py', target)
    run_script_in_venv(venv_path, 'url_scan.py', target)
    run_script_in_venv(venv_path, 'wordpress_scan.py', target)

    wpscan_json = f"wpscan_{target.replace('/', '_').replace(':', '_')}.json"
    summary_csv = f"wpscan_{target.replace('/', '_').replace(':', '_')}_summary.csv"
    run_script_in_venv(venv_path, 'summarize_wpscan.py', wpscan_json, summary_csv)

    run_script_in_venv(venv_path, 'vuln_scan.py', target)

    wapiti_json = f"wapiti_scan_{target.replace('/', '_').replace(':', '_')}.json"
    wapiti_summary_csv = f"wapiti_scan_{target.replace('/', '_').replace(':', '_')}_summary.csv"
    run_script_in_venv(venv_path, 'summarize_wapiti.py', wapiti_json, wapiti_summary_csv)

    run_script_in_venv(venv_path, 'setup_metasploit_rpc.py')

    cve_cwe_csv = f"cve_cwe_extraction_{target.replace('/', '_').replace(':', '_')}.csv"
    run_script_in_venv(venv_path, 'extract_cve_cwe.py', wapiti_json, cve_cwe_csv)

    if os.path.exists(cve_cwe_csv):
        output_results_csv = f"exploit_results_{target.replace('/', '_').replace(':', '_')}.csv"
        run_script_in_venv(venv_path, 'exploit_cve_cwe.py', cve_cwe_csv, target, output_results_csv)
    else:
        print(f"Le fichier {cve_cwe_csv} n'existe pas. Aucune CVE/CWE n'a été trouvée ou extraite.")

    run_script_in_venv(venv_path, 'exploit_appli.py', target)
    run_script_in_venv(venv_path, 'brute_force.py', target)
    run_script_in_venv(venv_path, 'resume_results.py', target)
    run_script_in_venv(venv_path, 'move.py', target)
    run_script_in_venv(venv_path, 'serveur_web.py', target)

if __name__ == "__main__":
    main()
