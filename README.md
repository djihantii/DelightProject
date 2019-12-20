# DelightProject
Test technique
Les deux projets sont indépendants.

**Monitoring**
Chaque jour ça extrait les commits du jour d'avant et calcule le nombre. <br>
Pour le moniroting je me suis basée sur le crontab de linux pour planifier l'extraction de données <br>
la source de données est 'https://api.github.com/repos/Facebook/commits?since=DATE_D_HIER' <br>
le script.sh sert à programmer alors le crontab. <br>

__Dependances__
requests
datetime
time
os


**Flask**
Pour extraires les données, les formatter puis les utiliser.
Pour cela il faut lancer un script pour lancer l'environnement virtuel et installer les différentes librairies utilisées pour le projet
__Les librairires sont__
flask
requests
json
matplotlib
pandas
datetime
time
os
io
calendar

**Pour le fonctionnement de l'api**
  *On extrait les données de 'https://api.github.com/repos/Facebook/react/stats/contributors'
  *En respectant les accept headers.
  *On les formatte => En créant une classe et en affectant chaque type de donnée à son attribut
  
  *On prend une date de début et date de fin, à partir de ces dates, on cherche la date du dimanche passé : car les semaines commencent par dimanche
  *On Fait des transformations sur les dates de timestamp en date et vice versa.
  *A partir des deux dates on calcule
    *Le nombre de commit de chaque contributeur dans cette période
    *On trie dans un ordre décroissant afin d'afficher les 9 premiers contributeurs dans cette période
    *Le pourcentage de chaque contributeur dans ce total de commits
    *On trace alors le graphe total + un graphe par contributeur pour la période précisée
    *Les graphes seront dans le dossier static, ils seront aussi affichés dans une page web en utilisant **flask**


