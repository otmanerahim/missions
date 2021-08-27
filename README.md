# PACMAN

![pacman image](https://img.redbull.com/images/c_limit,w_1500,h_1000,f_auto,q_auto/redbullcom/2020/7/8/xzlb8zjf9aghyiotbb1f/pac-man-screenshot)

Bonjour et bienvenue à tous les étudiants !

Cette suite de TP a spécialement été réalisé pour vous afin que vous puissiez mieux comprendre comment est réalisé l'intelligence derrière les personnages (Pinky, Blinky,...). Avouez que vous êtes impatients de comprendre comment sont réalisés ces IA qui donnent au jeu une expérience unique aux joueurs ! Cependant afin d'obtenir la version complète de pacman il faudra redoublez d'efforts et passez plusieurs obstacles ! Mais ne vous inquiétez à chaque TP vous serez guider par mes fameux conseils :)

# Les différents TPs :

Le but de ces différents TPS n'est pas de vous faire réaliser le jeu pacman en entier, mais que vous compreniez quelles sont les techniques qui sont utilisées pour améliorer une intelligence artificielle (je vous vois déjà fuir, n'ayez crainte voyons ! :) )

## TP1

Durant cette première partie de TP il vous faudra changez le comportement de Blinky pour qu'il aille dans la direction de pac-man (sans jamais faire machine arrière). A chaque fois qu'il arrive à une intersection, il choisit celle qui correspond le plus à la direction de pacman (sauf faire demi-tour).

## TP2

Changer le comportement de Pinky pour qu'il cherche systématiquement à atteindre la position située 4 cases devant pacman (cela dépend donc de la direction de pacman)

## TP3

Changer le comportement de Inky pour qu'il cible la position opposée à Blinky par rapport à pacman (symétrique par rapport à pacman)

## TP4

Changer le comportement de Clyde qui bouge de façon aléatoire tant qu'il est à plus de 8 cases de pacman et qui le cible (comme blinky) quand il est à moins de 8 cases

## TP5

Ajouter la notion d'état pour chaque ghost : chase et scatter (comme dans la vidéo), avec un timer pour chaque changement d'état (différent pour chaque ghost)

## TP6

Ajouter les fruits magiques et donc l'état frightened et eaten avec les comportements associés : frightened

## TP7

Pour se rapprocher de pacman original, copier le mouvement de "scatter" dans lequel les ghosts "patrouillent" dans un coin de l'écran

## TP8

Changer le mode "frightened" pour que les ghosts "fuient" pacman

## Lancement du jeu

Pour chaque TP il faut lancer le fichier run.py

## Prérequis

python3

```py
pip install python3
```

librairie pygame

```py
pip install pygame
```
