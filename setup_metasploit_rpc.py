import os
import subprocess
import time
from pymetasploit3.msfrpc import MsfRpcClient

def run_command(command):
    """Exécute une commande shell et renvoie le résultat."""
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de la commande : {' '.join(command)}")
        print(f"Code d'erreur : {e.returncode}")
        print(f"Sortie : {e.output}")
        exit(1)

def install_metasploit():
    """Installe Metasploit Framework si ce n'est pas déjà fait."""
    try:
        subprocess.run(["msfconsole", "--version"], check=True)
        print("Metasploit est déjà installé.")
    except subprocess.CalledProcessError:
        print("Metasploit n'est pas installé. Installation en cours...")
        run_command(["sudo", "apt-get", "update"])
        run_command(["sudo", "apt-get", "install", "-y", "metasploit-framework"])
        print("Metasploit a été installé avec succès.")

def install_pip():
    """Installe pip si ce n'est pas déjà fait."""
    try:
        subprocess.run(["pip", "--version"], check=True)
        print("pip est déjà installé.")
    except subprocess.CalledProcessError:
        print("pip n'est pas installé. Installation en cours...")
        run_command(["sudo", "apt-get", "install", "-y", "python3-pip"])
        print("pip a été installé avec succès.")

def install_pymetasploit3():
    """Installe pymetasploit3 via pip."""
    try:
        print("Installation de pymetasploit3...")
        run_command(["pip", "install", "pymetasploit3"])
        print("pymetasploit3 a été installé avec succès.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'installation de pymetasploit3 : {e}")
        exit(1)

def start_msfrpcd():
    """Démarre le service RPC de Metasploit avec msfrpcd."""
    print("Démarrage de msfrpcd (Metasploit RPC daemon)...")
    subprocess.Popen(["sudo", "msfrpcd", "-P", "msf", "-S"])
    
    print("Attente de 10 secondes pour que le service RPC démarre...")
    time.sleep(10)  # Attendre que le service RPC démarre

    # Vérification de la connexion au service RPC
    try:
        client = MsfRpcClient('msf', port=55553)  # Tenter la connexion
        print("Connexion au service RPC de Metasploit réussie.")
    except Exception as e:
        print(f"Erreur : Impossible de se connecter au service RPC de Metasploit. {e}")
        exit(1)

def main():
    install_metasploit()
    install_pip()
    install_pymetasploit3()
    start_msfrpcd()
    print("Configuration terminée. Le serveur RPC de Metasploit est en cours d'exécution.")
    print("Vous pouvez maintenant exécuter votre script Python.")

if __name__ == "__main__":
    main()
