# Projet SDV Toolbox

## CONTEXTE et OBJECTIFS DU PROJET

    Doli Industry est une entreprise industrielle opérant à l'échelle internationale, qui cherche à renforcer la sécurité de ses systèmes d'information en automatisant ses tests d'intrusion. Actuellement, les tests sont réalisés manuellement, ce qui est long, couvre une portée limitée et rend l'analyse des résultats complexe.

    Objectifs du projet : Développer une toolbox automatisée pour les tests d'intrusion afin de :

    - Réduire les coûts en automatisant certaines tâches.
    - Accélérer la réalisation des tests pour des contrôles de sécurité plus fréquents.
    - Améliorer la couverture des tests pour identifier un plus grand nombre de vulnérabilités.
    - Simplifier l'analyse grâce à des rapports détaillés et des visualisations.
    - Portée du projet : Le projet se concentrera sur le développement de la toolbox elle-même, qui intégrera plusieurs outils de tests d'intrusion.

## Description
    Ce projet est une boîte à outils automatisée de tests de sécurité pour une cible spécifique, telle qu'une application web ou un serveur. Il utilise plusieurs outils de sécurité (Nmap, Gobuster, WPScan, Wapiti, etc.) pour effectuer une analyse complète des vulnérabilités et en extraire des résultats exploitables. Le projet génère un rapport sous forme de fichiers CSV et propose également un serveur web pour visualiser les résultats sous forme de tableaux et graphiques. L'avantage premier de ce projet est qu'il n'y a rien à installer ni à configurer pour l'utilisateur, il suffit de télécharger ce github et de lancer app.py.

## Prérequis
- Système d'exploitation : Kali Linux à jour téléchargeable ici : https://www.kali.org/get-kali/#kali-virtual-machines
- Aucune restriction de flux ne doit s'appliquer sur l'environnement Kali utilisé 
- Execution avec un utilisateur ayant les droits de lecture et d'écriture

#######################################Présentation de l'architecture#########################################

projet_sdv_toolbox/				                      # Répertoire racine du projet
├── static/                        					  # Dossier pour les fichiers statiques (CSS, JS, images)
│   ├── style.css                  					  # Feuille de style pour la mise en forme de l'interface web
│   ├── pdf_style.css                  			      # Feuille de style pour la mise en forme du pdf
│   └── script.js                  					  # Fichier JavaScript pour les fonctionnalités dynamiques du tableau de bord
├── templates/                     					  # Dossier pour les templates HTML du serveur web
│   └── index.html                 					  # Template principal pour afficher les résultats sur la page web
└── results/                                          # Dossier contenant les résultats des scans et analyses
├── app.py                     						  # Script principal qui exécute tous les autres scripts
├── bruteforce.py               					  # Script pour effectuer des attaques de brute force
├── exploit_appli.py            					  # Exploite des vulnérabilités liées aux applications
├── exploit_cve_cwe.py          					  # Exploite les CVE et CWE trouvées
├── extract_cve_cwe.py          					  # Extrait les CVE et CWE des résultats de scan
├── move.py                     					  # Déplace les fichiers de résultats dans des dossiers spécifiques
├── nmap_scan.py                					  # Effectue un scan Nmap
├── README.md                   					  # Fichier d'explication du projet (à compléter)
├── resume_results.py           					  # Crée un résumé des résultats des différents scans
├── serveur_web.py              				      # Lancement du serveur web Flask pour afficher les résultats
├── setup_metasploit_rpc.py      					  # Configure le service RPC de Metasploit
├── summarize_wapiti.py         					  # Résume les résultats du scan Wapiti dans un fichier CSV
├── summarize_wpscan.py         					  # Résume les résultats du scan WPScan dans un fichier CSV
├── url_scan.py                 					  # Effectue un scan de répertoires à l'aide de Gobuster
├── vuln_scan.py                					  # Lance Wapiti pour analyser les vulnérabilités web
├── whatweb.py                 						  # Identifie les technologies et applications d'un site web
├── wordpress_scan.py           					  # Lance WPScan sur un site WordPress
├── results/                       					  # Répertoire où sont déplacés tous les fichiers de résultats pour une cible donnée
│   └── target_date/               					  # Sous-répertoire pour chaque cible (target) et date du scan
│       ├── nmap_scan_target.csv               	      # Résultats du scan Nmap
│       ├── gobuster_scan_target_80.csv        	      # Résultats du scan Gobuster pour le port 80
│       ├── gobuster_scan_target_443.csv       	      # Résultats du scan Gobuster pour le port 443
│       ├── wpscan_target.json                 	      # Résultats du scan WPScan
│       ├── wpscan_target_summary.csv          	      # Résumé des résultats WPScan
│       ├── wapiti_scan_target.json            	      # Résultats du scan Wapiti
│       ├── wapiti_scan_target_summary.csv     	      # Résumé des résultats Wapiti
│       ├── cve_cwe_extraction_target.csv          	  # Extraction des CVE et CWE détectées
│       ├── exploit_results_target.csv         	      # Résultats des exploits tentés
│       ├── brute_force_results_target.csv      	  # Résultats des tentatives de brute force
│       ├── whatweb_results_target.csv         	      # Résultats du scan WhatWeb
│       ├── metasploit_app_target.csv                         # Résultats des exploits Metasploit pour les applications détectées
│       ├── summary_results_target.csv                        # Résumé général des résultats

####################################Fin de présentation de l'architecture#####################################

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
   
   Veuillez entrer l'adresse IP ou le nom DNS de la cible : 192.168.0.1 ou glpi.cybersdv.fr
   

   Le script exécutera ensuite les différents outils et produira des fichiers CSV contenant les résultats des analyses. Un serveur web sera également démarré pour afficher un tableau de bord avec les résultats.

4. Accéder aux résultats :
   Les résultats des analyses sont enregistrés dans le dossier 'results', qui contient un sous-dossier avec le nom de la cible et la date d'exécution. Pour visualiser les résultats dans un navigateur, un serveur Flask sera automatiquement lancé et accessible à l'adresse suivante :
   
   http://127.0.0.1:5000


### Rappel des commandes        ###

  - sudo git clone https://github.com/simonjacquot/projet_sdv_toolbox.git
  - cd projet_sdv_toolbox
  - sudo python app.py           
# Temps moyen d'attente pour la réalisation 15 min
# Ouverture automatique du rapport à l'adresse suivante http://127.0.0.1:5000

### Fin de rappel des commandes ###
  
