import os
import subprocess
import time
from pymetasploit3.msfrpc import MsfRpcClient

def run_command(command):
    """
    Exécute une commande shell et vérifie son succès.

    Args:
        command (list): Liste des commandes et arguments à exécuter.
    """
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de la commande : {' '.join(command)}")
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

def install_pip():
    """
    Vérifie si pip est installé. Si non, l'installe.
    """
    try:
        subprocess.run(["pip", "--version"], check=True)
        print("pip est déjà installé.")
    except subprocess.CalledProcessError:
        print("pip n'est pas installé. Installation en cours...")
        run_command(["sudo", "apt-get", "install", "-y", "python3-pip"])
        print("pip a été installé avec succès.")

def install_pymetasploit3():
    """
    Installe la bibliothèque pymetasploit3 pour interagir avec l'API de Metasploit.
    """
    try:
        print("Installation de pymetasploit3...")
        run_command(["pip", "install", "pymetasploit3"])
        print("pymetasploit3 a été installé avec succès.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'installation de pymetasploit3 : {e}")
        exit(1)

def start_msfrpcd():
    """
    Démarre le service RPC de Metasploit (msfrpcd) pour permettre les interactions avec l'API.
    """
    print("Démarrage de msfrpcd (Metasploit RPC daemon)...")
    subprocess.Popen(["sudo", "msfrpcd", "-P", "msf", "-S"])
    
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
    Fonction principale pour installer Metasploit, pip, pymetasploit3, et démarrer le service RPC.
    """
    install_metasploit()      # Installation de Metasploit Framework
    install_pip()             # Installation de pip si nécessaire
    install_pymetasploit3()   # Installation de pymetasploit3
    start_msfrpcd()           # Démarrage du service RPC de Metasploit
    print("Configuration terminée. Le serveur RPC de Metasploit est en cours d'exécution.")
    print("Vous pouvez maintenant exécuter votre script Python.")

if __name__ == "__main__":
    main()
