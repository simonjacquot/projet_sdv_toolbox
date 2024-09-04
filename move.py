import os
import shutil
from datetime import datetime

def create_target_directory(target):
    """Crée un dossier au nom de la cible et de la date actuelle dans le dossier 'results'."""
    date_str = datetime.now().strftime('%Y-%m-%d')
    base_directory = "results"
    directory_name = os.path.join(base_directory, f"{target}_{date_str}")

    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
        print(f"Dossier créé: {directory_name}")
    else:
        print(f"Le dossier {directory_name} existe déjà.")
    
    return directory_name

def move_files_to_directory(target, directory_name):
    """Déplace les fichiers liés à la cible dans le dossier créé."""
    files_to_move = [
        f"nmap_scan_{target}.csv",
        f"gobuster_scan_{target}.csv",
        f"gobuster_scan_{target}_80.csv",
        f"gobuster_scan_{target}_443.csv",
        f"gobuster_scan_{target}_8080.csv",
        f"gobuster_scan_{target}_8443.csv",
        f"wpscan_{target}.json",
        f"wpscan_{target}_summary.csv",
        f"wapiti_scan_{target}.json",
        f"wapiti_scan_{target}_summary.csv",
        f"cve_cwe_extraction_{target}.csv",
        f"exploit_results_{target}.csv",
        f"brute_force_results_{target}.csv",
        f"sqlmap_results_{target}.csv",
        f"cve_cwe_analysis_{target}.csv",
        f"whatweb_results_{target}.csv",
        f"metasploit_app_{target}.csv",
        f"summary_results_{target}.csv"
    ]

    for file_name in files_to_move:
        if os.path.exists(file_name):
            shutil.move(file_name, os.path.join(directory_name, file_name))
            print(f"Fichier déplacé: {file_name} vers {directory_name}")
        else:
            print(f"Fichier non trouvé: {file_name}")

def main(target):
    """Fonction principale pour créer le dossier et déplacer les fichiers."""
    directory_name = create_target_directory(target)
    move_files_to_directory(target, directory_name)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python move_files.py <target>")
        sys.exit(1)

    target = sys.argv[1]
    main(target)
