# Projet SDV Toolbox

## Description
Ce projet est une boîte à outils automatisée de tests de sécurité pour une cible spécifique, telle qu'une application web ou un serveur. Il utilise plusieurs outils de sécurité (Nmap, Gobuster, WPScan, Wapiti, etc.) pour effectuer une analyse complète des vulnérabilités et en extraire des résultats exploitables. Le projet génère un rapport sous forme de fichiers CSV et propose également un serveur web pour visualiser les résultats sous forme de tableaux et graphiques.

## Prérequis
- Système d'exploitation : Kali Linux (ou toute autre distribution basée sur Debian)
- Python : version 3.11 ou supérieure
- Bibliothèques Python :
  - 'pymetasploit3'
  - 'Flask'
  - 'Pandas'
  - 'Nmap'
  - etc. (gérées via 'requirements.txt')
- Outils de sécurité :
  - Nmap
  - Gobuster
  - WPScan
  - Wapiti
  - Metasploit Framework

## Instructions d'installation
Pour lancer le projet, il suffit de cloner ce dépôt sur une nouvelle machine Kali Linux, puis d'exécuter le script principal 'app.py', qui se chargera automatiquement de l'installation des dépendances et du lancement des analyses.

1. Télécharger le projet :
 
   git clone https://github.com/simonjacquot/projet_sdv_toolbox.git
   cd projet_sdv_toolbox
   

2. Lancer l'analyse :
   Le script 'app.py' va automatiquement :
   - Installer les outils nécessaires (via 'apt-get')
   - Créer un environnement virtuel Python
   - Installer les dépendances Python (via 'requirements.txt')
   - Lancer une série d'analyses de sécurité sur la cible spécifiée.

   Pour démarrer :
   sudo python app.py
   

3. Exemple d'utilisation :
   Lors du lancement, il vous sera demandé de fournir l'adresse IP ou le nom DNS de la cible.
   
   Veuillez entrer l'adresse IP ou le nom DNS de la cible : 192.168.0.1
   

   Le script exécutera ensuite les différents outils et produira des fichiers CSV contenant les résultats des analyses. Un serveur web sera également démarré pour afficher un tableau de bord avec les résultats.

4. Accéder aux résultats :
   Les résultats des analyses sont enregistrés dans le dossier 'results', qui contient un sous-dossier avec le nom de la cible et la date d'exécution. Pour visualiser les résultats dans un navigateur, un serveur Flask sera automatiquement lancé et accessible à l'adresse suivante :
   
   http://127.0.0.1:5000
