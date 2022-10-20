# Journal de bord

## 2022.09.15
Vu que je ne fait plus le projet VR avec rami, je doit refaire un cahier des charges pour mon projet solo.

Je prépare déjà Rapberry Pi Imager pour la semaine prochaine.

## 2022.09.22
J'ai installé une installation clean de Raspberry Pi OS. Je vais surtout regarder quelques tutos pou voir comment intéragir avec le CrowPi et commencer à faire le poster.

J'ai essayer le code de démo du LCD mais on me dit que j'ai pas la librairie et j'en installe une mais, soit j'ai installé la mauvaise, soit la librairie à beaucoup changée, mais je n'arrive pas à le faire fonctionner.

## 2022.09.29
Ce qui est bizzare c'est que les pin de la criox  marquées dans le circuit du CrowPi et celles qui faut utiliser dans le programme sont différentes. Par exemple, pour le bouton haut ça dit qu'il faut utiliser la pin 37 mais dans le programme c'est la pin 26.

Il y a le même problème que chez moi ou pygame sur Linux à l'air de crasher quand on quitte.

Problême réglé, c'est que je reset le GPIO et après j'en utilise une.

Après avoir vu la doc, RPi.GPIO.BCM met les Pin dans un ordre différent.

J'ai réussi à faire intéragir les GPIO et pygame

## 2022.10.06
J'ai pu faire en sorte qu'un bouton ne puisse pas faire constament une action quand un boutton est maintenu.

## 2022.10.20
J'ai décidé de mettre le code de l'énigme que j'ai fair dans une fonction à part et en laissant la variable qui contient la tentative dehors, mais ça me retourne une erreur qui me dit que la variable est référencée avant d'être assignée. Ce qui est fait exprès.

Je pense savoir où est le problème, j'ai passé la variable en local mais maintenant une autre variable qui sert à empécher le code de prendre en compte le bouton s'il est maintenu revoir la même erreur Ce qui veut dire que le code ignore les variables global.

J'ai trouvé la solûtion. Je devais juste déclarer que ces variables étaient globales au début de la fonction.

J'ai essayé d'exécuter le script de démo de la matrice LED, mais même après avoir installé les librairies qui faut, il n'arrive pas à utiliser le SPI pour communiquer avec la matrice.
