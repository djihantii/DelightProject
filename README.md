# DelightProject
Test technique
Les deux projets sont indépendants.

**Monitoring**
Chaque jour ça extrait les commits du jour d'avant et calcule le nombre. <br>
Pour le moniroting je me suis basée sur le crontab de linux pour planifier l'extraction de données <br>
la source de données est 'https://api.github.com/repos/Facebook/commits?since=DATE_D_HIER' <br>
le script.sh sert à programmer alors le crontab. <br>
<br><br>
__Dependances__ <br>
requests <br>
datetime <br>
time <br>
os <br>
<br>
<br>
<br>

**Flask** <br>
Pour extraires les données, les formatter puis les utiliser. <br>
Pour cela il faut lancer un script pour lancer l'environnement virtuel et installer les différentes librairies utilisées pour le projet <br><br><br>
__Les librairires sont__<br>
flask<br>
requests<br>
json<br>
matplotlib<br>
pandas<br>
datetime<br>
time<br>
os<br>
io<br>
calendar<br>
<br><br><br><br>
**Pour le fonctionnement de l'api**<br>
  *On extrait les données de 'https://api.github.com/repos/Facebook/react/stats/contributors'<br>
  *En respectant les accept headers.<br>
  *On les formatte => En créant une classe et en affectant chaque type de donnée à son attribut<br>
  *On prend une date de début et date de fin, à partir de ces dates, on cherche la date du dimanche passé : car les semaines commencent par dimanche<br>
  *On Fait des transformations sur les dates de timestamp en date et vice versa.<br>
  *A partir des deux dates on calcule<br>
    *Le nombre de commit de chaque contributeur dans cette période<br>
    *On trie dans un ordre décroissant afin d'afficher les 9 premiers contributeurs dans cette période<br>
    *Le pourcentage de chaque contributeur dans ce total de commits<br>
    *On trace alors le graphe total + un graphe par contributeur pour la période précisée<br>
    *Les graphes seront dans le dossier static, ils seront aussi affichés dans une page web en utilisant **flask**<br><br>


