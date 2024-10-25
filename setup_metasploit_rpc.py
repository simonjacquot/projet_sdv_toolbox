import os
import subprocess
import time
from pymetasploit3.msfrpc import MsfRpcClient

def run_command(command, use_shell=False):
    """
    Exécute une commande shell et vérifie son succès.

    Args:
        command (list/str): Liste des commandes et arguments à exécuter.
        use_shell (bool): Indique si la commande doit être exécutée dans un shell.
    """
    try:
        if use_shell:
            subprocess.run(command, shell=True, check=True, executable="/bin/bash")
        else:
            subprocess.run(command, check=True)
        print(f"Commande '{command}' exécutée avec succès.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de la commande : {command}")
        print(f"Code d'erreur : {e.returncode}")
        print(f"Sortie : {e.output}")
        exit(1)

def install_metasploit():
    """
    Vérifie si Metasploit Framework est installé. Si non, l'installe.
    """
    try:
        subprocess.run(["msfconsole", "--version"], check=True)
        print("Metasploit est déjà installé.")
    except subprocess.CalledProcessError:
        print("Metasploit n'est pas installé. Installation en cours...")
        run_command(["sudo", "apt-get", "update"])
        run_command(["sudo", "apt-get", "install", "-y", "metasploit-framework"])
        print("Metasploit a été installé avec succès.")

def install_pymetasploit3_in_venv():
    """
    Installe la bibliothèque pymetasploit3 pour interagir avec l'API de Metasploit
    dans l'environnement virtuel.
    """
    venv_path = os.path.abspath("venv")
    python_venv = os.path.join(venv_path, "bin", "pip")
    
    try:
        print("Installation de pymetasploit3 dans l'environnement virtuel...")
        run_command([python_venv, "install", "pymetasploit3"])
        print("pymetasploit3 a été installé avec succès dans l'environnement virtuel.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'installation de pymetasploit3 : {e}")
        exit(1)

def start_msfrpcd():
    """
    Démarre le service RPC de Metasploit (msfrpcd) pour permettre les interactions avec l'API.
    """
    print("Démarrage de msfrpcd (Metasploit RPC daemon)...")
    subprocess.Popen(["sudo", "msfrpcd", "-P", "msf", "-S", "-p", "55553"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    print("Attente de 10 secondes pour que le service RPC démarre...")
    time.sleep(10)  # Attendre 10 secondes pour laisser le service démarrer

    # Vérification de la connexion au service RPC
    try:
        client = MsfRpcClient('msf', port=55553)  # Connexion au RPC avec le mot de passe msf
        print("Connexion au service RPC de Metasploit réussie.")
    except Exception as e:
        print(f"Erreur : Impossible de se connecter au service RPC de Metasploit. {e}")
        exit(1)

def main():
    """
    Fonction principale pour installer Metasploit, pymetasploit3, et démarrer le service RPC.
    """
    install_metasploit()          # Installation de Metasploit Framework
    install_pymetasploit3_in_venv()  # Installation de pymetasploit3 dans le venv
    start_msfrpcd()               # Démarrage du service RPC de Metasploit
    print("Configuration terminée. Le serveur RPC de Metasploit est en cours d'exécution.")
    print("Vous pouvez maintenant exécuter votre script Python.")

if __name__ == "__main__":
    main()
