# Journal de bord

## 2022.09.15
Vu que je ne fais plus le projet VR avec Rami, je dois refaire un cahier des charges pour mon projet solo.

Je prépare déjà Rapberry Pi Imager pour la semaine prochaine.

## 2022.09.22
J'ai installé une installation clean de Raspberry Pi OS. Je vais surtout regarder quelques tutos pou voir comment interagir avec le CrowPi et commencer à faire le poster.

J'ai essayé le code de démo du LCD mais on me dit que je n'ai pas la librairie et j'en installe une mais, soit j'ai installé la mauvaise, soit la librairie à beaucoup changée, mais je n'arrive pas à le faire fonctionner.

## 2022.09.29
Ce qui est bizarre c'est que les pins de la croix marquée dans le circuit du CrowPi et celles qui faut utiliser dans le programme sont différentes. Par exemple, pour le bouton haut ça dit qu'il faut utiliser la PIN 37 mais dans le programme c'est la PIN 26.

Il y a le même problème que chez moi ou pygame sur Linux à l'air de crasher quand on quitte.

Problème réglé, c'est que je reset le GPIO et après j'en utilise une.

Après avoir vu la doc, RPi.GPIO.BCM met les Pin dans un ordre différent.

J'ai réussi à faire interagir les GPIO et pygame

## 2022.10.06
J'ai pu faire en sorte qu'un bouton ne puisse pas faire constamment une action quand un boutton est maintenu.

## 2022.10.20
J'ai décidé de mettre le code de l'énigme que j'ai fair dans une fonction à part et en laissant la variable qui contient la tentative dehors, mais ça me retourne une erreur qui me dit que la variable est référencée avant d'être assignée. Ce qui est fait exprès.

Je pense savoir où est le problème, j'ai passé la variable en local mais maintenant une autre variable qui sert à empêcher le code de prendre en compte le bouton s'il est maintenu revoir la même erreur Ce qui veut dire que le code ignore les variables globales.

J'ai trouvé la solution. Je devais juste déclarer que ces variables étaient globales au début de la fonction.

J'ai essayé d'exécuter le script de démo de la matrice LED, mais même après avoir installé les librairies qui faut, il n'arrive pas à utiliser le SPI pour communiquer avec la matrice.

## 2022.11.03
Aujourd'hui mon objectif est de créer une énigme ou il faut crier au bon volume.

En regardant j'ai vu qu'à partir de Python 3.10, le language possède un équivalent au switch case avec match, mais la version de Raspberry Pi OS est encore en 3.9.2, donc je vais plutôt utiliser les elif en cascade.

J'abandonne l'idée du micro car les GPIO ne sont que digitale. A la place j'aurais une énigme qui utilise le capteur de distance.

![Le capteur de distance à ultrason](./img/capt-dist.jpg){: style="height:300px"}

J'ai pu afficher du texte avec pygame. C'est facile mais il y a un peu de boilerplate code. Il faut créer un objet pour la police, puis pour le texte et un rectangle pour le texte.

``` python
font = pygame.font.sysFont('freesansbold.ttf', 32) # Initialiser la police
text = font.Render('Vies : 3', True, (0, 0, 0)) # Créer l'objet texte
text_rect = text.get_rect() # Obtenir la boîte pour afficher le texte
screen.blit(text, text_rect) # Afficher le texte
```

En essayent de push les changements d'aujourd'hui je me rends compte que j'ai oublié de pull avant de commencer et j'ai un conflit que j'ai besoin de résoudre.

## 2022.11.10
Honnêtement résoudre un conflit avec Vim était plutôt simple.

Aujourd'hui, mon objectif est de créer une troisième voir une quatrième énigme.

Pour ma troisième énigme, je pensais à devoir écrire un message en Morse avec le détecteur de toucher.

![détecteur de touché](./img/capt-touch.jpg){: style="height:300px"}

J'ai un peu modifié le code de la deuxième énigme pour affiche un vague message qui dit si on est trop haut ou trop bas au lieu de la distance elle-même.

# 2022.11.17
J'ai un peu regarder comment calculer un intervalle de temps qu'un bouton est pressé, et quand je rajoute un bool pour ne pas inonder la console, ça me met des résultats incorrectes.

J'ai mis le code dans un callback et ça fonctionne

# 2022.11.19
Vu que je dois vérifier deux chaînes de la même manière, j'ai mis le code dans une fonction séparée.

Pour gérer le callback, j'ai mis la variable en globale que je vérifie pour voir si la valeur est supérieure à 0, puis je regarde la durée pour déterminer si c'est un cours (.) ou un long (-)

Quand je fais un long, il est reconnu mais quand je fais un cours, il ne se passe rien.

J'avais mis un temps pas assez intuitif pour un cours, pour finir, maintenir ~200 ms est un appui court, et ~ 600 ms est un appui long.

## 2022.11.20
Je vais me concentrer sur l'interface, la qualité du code et la documentation car je ne pense pas pouvoir faire tout ça et une nouvelle énigme.

J'ai ajouté un texte pour donner le contexte de l'énigme et un indice si on échoue trop de fois.

J'ai ajouté un écran de fin.

![écran de fin](./img/end-screen.png){: style="height:300px"}

Je viens de me rendre compte que chaque lignes ou j'appelle `get_rect()` se finies par un ;