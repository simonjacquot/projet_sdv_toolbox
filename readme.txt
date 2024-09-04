  Téléchargement :
git clone https://github.com/simonjacquot/projet_sdv_toolbox.git
cd projet_sdv_toolbox

  Installation :
apt install python3.11-venv
apt-get install gobuster
apt-get install wpscan

python -m venv venv                  ####Création du venv python
source venv/bin/activate             ####faire cette commande avant de faire les pip install et de faire lancer le script

pip install -r requirements.txt      #####Installation des prérequis

python app.py                        #####lancement du script maître qui lancera par la suite l'ensemble des scripts


  Rappel fonctionnement :

1. app.py                            #####Script maître
2. lancement auto de nmap scan (scan des ports et génération d'un rapport csv)
3. lancement auto de gobuster scan (scan des url et génération d'un rapport csv)
4. lancement auto de wp scan (scan des vulnérabilités s'il s'agit d'un wordpress et génération d'un json et conversion résumé en csv)
5. lancement auto de wapiti scan (scan des vulnérabilités d'un serveur web s'il a détecté un serveur web dans le csv de nmap et génération d'un json et conversion résumé en csv)

Suite à apporter :
1. ajout d'un script pour exploiter les vulnérabilités du csv/json généré par wapiti (Métasploit est pas mal !)
2. Création d'un site html/css/js qui va lire les résultats et les présenter proprement (tableau/dashboard)
3. Changement de l'ensemble des scripts pour que les rapports csv et json se créé dans un dossier du nom de la cible
4. Ajout d'une boîte de dialogue graphique pour la saisie de l'ip/dns cible
5. ....

