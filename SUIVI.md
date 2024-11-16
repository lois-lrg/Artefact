# Suivi du projet

## TODO

- **Séance 2 :**
  - Se familiariser avec GITLAB et les clés SSH
  - Répartir les tâches nécessaires à l'avancement dans le projet
  - Attribuer des responsables sur les différentes tâches
- **Séance 3 :**
  - Connecter la Raspberry Pi au Wifi de l'école (réseau "Campus-Télécom")
  - mettre la carte à l'heure vie le serveur ntp de l'école voir déroulé de la séance (https://discourse.r2.enst.fr/docs?topic=408)
  - Tester les moteurs et la carte de contrôle
  - Tester la caméra
  - Faire le design de notre robot  
- **Séance 4 :**
  - Avancer dans les différentes tâches
  - Commencer la réflexion sur l'architecture logicielle du projet.  
- **Séance 5 :**
  - Finir l’assemblage du robot
  - Faire les premiers tests de moteurs sur le robot
  - Continuer le développement des différentes tâches
  - Définir l’architecture logicielle de votre projet.
- **Séance 6 :**
  - Continuer le développement des différentes tâches
  - Intégrer vos tests dans le script de test `tests_projet.sh` en racine de votre dépôt Git.
  - Définir l’architecture logicielle de votre projet.
- **Séance 7 :**  
Avant la séance:  
  - Le script de test est fonctionnel pour chacun des modules développés, mais les tests peuvent ne pas être encore valides.   
 
  Pendant cette séance vous devrez:

  - continuer le développement des différentes tâches
  - corriger les résultats de vos scripts de test
  - commencer à mettre en place votre architecture logicielle  

  Les séances 8 et 9 étant consacrés à l’intégration, il est très important d’arriver en séance 8 sans « trous dans la raquette ».
- **Séance 8 :**
  - Intégration et tests pour l’évaluation intermédiaire
- **Séance 9 :**
  - Intégration et tests pour l’évaluation intermédiaire
- **Séance 10 - EVALUATION INTERMEDIAIRE !!! :**  
  
  - Savoir se déplacer manuellement (mini-parcours)
  - Savoir se déplacer dans un damier automatiquement: point de départ fixe, point d’arrivée communiqué par le jury
  - Savoir trouver une balise simple (faisant face au point de départ) et s’en approcher à 20-40 cm
  - Savoir trouver une balise complexe (non orientée vers le point de départ) et s’en approcher à 20-40 cm  


  Description précise de l'évaluation : 

  - Envoyer au serveur de suivi sa position estimée (envoi une fois par seconde)
  - Attention à la luminosité de la salle pour la reconnaissance des codes Aruco.
  
  Epreuve de pilotage :
  - Robot piloté jusqu'à la ligne de départ via un parcours simple en mode manuel

  Epreuve de conduite autonome :
  - Le jury donne une case où doit se rendre le robot, l'équipe entre cette case ex B3 dans le robot puis quand passage en mode automatique appuyé, le robot s'y rend tout seul avant de faire un tour sur lui même une fois arrivé.
  
  Chasse au drapeaux autonome :
  - Positionnement sur la ligne de départ
  - positionnement de deux drapeaux : 1 face visible (le plus proche), l'autre face caché (le plus éloigné).
  - Le jury donne le départ
  - Bascule en mode autonome
  - Le robot doit aller capturer seul les deux drapeaux et faire un tour complet sur lui même une fois réussi
  

    
      
## AVANCEMENT

### Séance 1

Découverte du site : https://proj103.telecom-paris.fr  
Vérification et découverte du matériel  

**A faire pour la séance suivante** -> lire l’UE gitlab, https://outils101.telecom-paris.fr/  
  
### Séance 2 

Configuration des clés ssh et des comptes pour tous les membres du groupe de manière à être opérationnel pour mettre à jour et gérer le versionnement via GIT.  
Ajout de l’OS sur la clé usb pour la Raspberry PI :
- installation de l'imager Raspberry Pi https://www.raspberrypi.com/software/   
- Installation de Raspberry Pi OS Lite en version 64-bits avec la configuration Wifi nécessaire et les paramètres SSH de sorte à pouvoir s’y connecter.  
- Impossible de connecter la Raspberry Pi au wifi directement nous sommes donc passés par le filaire et règlerons la connexion wifi une fois connectés en SSH.  

Liste des tâches nécessaires pour ce projet : 

- Contrôle des moteurs (Oscar)
- Interface web simplifiée (Loïs)
- Mini serveur Web pour contrôle manuel (Timothée)
- Dialogue avec le serveur web de suivi de déplacement (Alexis)
- Reconnaissance des codes ArUco avec la caméra et évaluation de la distance (Wassim)
- Design de la voiture / découpe laser du châssis etc (Timothée)


**A faire pour la séance suivante** -> Continuer de s'entrainer à la gestion de gitlab et des différentes commandes. 


### Séance 3

Nous avons testé la caméra directement depuis un PC. Celle-ci fonctionne sans problème et possède une qualité d'image très satisfaisante.  

Nous avons bien avancé le design de notre robot dans le but de faire un SVG pour la séance prochaine.

Nous avons également réussi à mettre à l'heure la carte depuis le serveur ntp de l'école.

Nous n'avons en revanche pas eu le temps de tester la carte de commande des moteurs et les moteurs. Nous nous sommes néanmoins renseignés sur le fonctionnement de ceux-ci, l'alimentation et la récupération des données des capteurs présents sur le moteur. Il ne restera plus qu'à créer un premier code permettant de piloter nos moteurs depuis la carte Raspberry. (Se renseigner sur I2C) 

**A faire pour la séance suivante** ->
- Terminer le SVG pour lancer la découpe de notre chassis **(Mettre le SVG sur la branche main de notre Git)**
- Prendre contact avec le tuteur par mail pour convenir d'un moment pour confirmer le chassis
- Eventuellement s'interesser à comment faire le petit programme pour commander le test des moteurs **(Interêt particulier pour le bus I2C)**


### Séance 4

Nous nous sommes mis d'accord pour le design du châssis du véhicule et avons presque terminé les plans et les modèles sur fusion 360. Nous avons donc les pièces principales de notre châssis à réaliser avec du bois grâce à la découpeuse laser du fablab et de petits raccords à faire sur imprimante 3D.

Nous avons également pu faire tous les tests nécessaires pour la prise en main des moteurs et vérifié que tout fonctionnait. On a aussi pu commencer à comprendre les codes de commandes moteur pour voir comment ils fonctionnaient et commencer à préparer les séances de codages qui vont venir.

**À faire pour la séance suivante** ->
- Terminer le SVG pour lancer la découpe de notre châssis **(Mettre le SVG sur la branche main de notre Git)**
- Voir pour faire la découpe laser de sorte à avoir un châssis opérationnel pour la prochaine séance.

### Séance 5

Ayant pris un peu de retard durant les précédentes séances, nous avons terminé le modèle 3D de notre robot et nous sommes allés voir le responsable du FabLab pour la découpe de notre support. Nous avons précédemment, lors d'un rendez-vous organisé entre les membres du groupe, réalisé les petites pièces de maintien via impression 3D.   
Nous avons donc réalisé le montage complet de notre robot et reparti les tâches à faire durant les prochaines séances :



**À faire pour la séance suivante** ->
- Se renseigner sur les différentes choses nécessaire pour la validation de la première évaluation. 

### Séance 6

Notre robot étant entièrement conçu, nous nous sommes penchés sur la répartition des tâches et avons commencé à travailler chacun de notre côté de manière à avancer celles-ci.

  - Alexis et Timothée : API et gestion de l'interconnexion entre l'interface web et la commande moteurs
  - Wassim : Reconnaissance des codes Aruco avec OpenCV
  - Oscar : Commande moteur
  - Loïs : interface web simplifiée avec créations de boutons (avancer, reculer, droite, gauche) pour le contrôle manuel du robot.

**À faire pour la séance suivante** ->
- Lister de manière plus exhaustive les critères d'évaluation intermédiaire.

### Séance 7


**À faire pour la séance suivante** ->

