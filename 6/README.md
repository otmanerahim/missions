# TP6

Dans ce TP vous allez devoir ajouter les fruits magiques et l'état **"freightened"** avec son comportement associé et l'état **"eaten"**.

L'état frightened représente l'état où les fantômes sont "gelés" et vulnérable après que pacman mange un super fruit ! Durant cet état pacman peut tuer les fantômes et gagner des points ! Une fois que pacman tue ces fantômes, les fantômes passent à un état "eaten" durant lequel ils retournent à leur case de départ.

La première chose à faire est de rajouter le nouvel état freight !

Pour ce faire vous allez modifier cette fonction qui servira uniquement à rajouter un nouvel état freight à notre pile !

```py
def freightMode(self):
        #
```

Puis vous allez modifier la fonction update des fantômes afin de prendre en compte cet état et donner un objectif aléatoire à nos fantômes lorsqu'ils rentrent dans cet état.

```py
def update(self, dt,pacman):
```

Dans le fichier run.py vous allez devoir modifier deux fonctions !

```py
 def checkPelletEvents(self):
    pellet = self.pacman.eatPellets(self.pellets.pelletList)
    if pellet:
        pygame.mixer.Sound.play(self.eat_sound)
        self.pelletsEaten += 1
        self.score += pellet.points
        self.pellets.pelletList.remove(pellet)
        if pellet.name == "powerpellet":
            self.ghosts.resetPoints()
        if self.pellets.isEmpty():
            self.pacman.visible = False
            self.ghosts.hide()
            self.pause.startTimer(3, "clear")
            self.flashBackground = True
```

Vous n'avez pour l'instant pas eu à modifier cette fonction, car depuis le début des TPs la pastille qui octroie la possibilité au pacman de tuer les fantômes n'était pas fonctionnelle, c'est dans cette fonction que le jeu note les évènements liés aux pastilles ! Cependant maintenant il faudra la modifier pour changer l'état des fantômes en freightened lorsque la pastille "powerpellet" est mangée.

Passons maintenant aux fruits ! Vous aurez une nouvelle classe fruit qui sera déjà créée qui sert uniquement à gérer les positions des fruits et leur apparition et disparition dans la carte. Vous allez devoir créer une nouvelle fonction qui gère les évènements avec les fruits comme vous avez pu le voir avec les pastilles !

```py
def checkFruitEvents(self):
   # à completer
```

Maintenant passons à l'état eaten !

```py
def checkGhostEvents(self):
  self.ghosts.release(self.pelletsEaten)
  ghost = self.pacman.eatGhost(self.ghosts)
  if ghost is not None:
      if ghost.mode.name == "FREIGHT":
          pygame.mixer.Sound.play(self.eatghost_sound)
          # à compléter
      elif ghost.mode.name != "SPAWN":
          pygame.mixer.Sound.play(self.death_sound)
          self.pacman.loseLife()
          self.ghosts.hide()
          self.pause.startTimer(3, "die")
```

Cette fonction gère les évènements liés aux fantômes, c'est ici que nous allons rajouter le code permettant de gérer la mort d'un fantôme ! Le code est simple si pacman tue un fantôme et que celui-ci est en état "FREIGHT" alors... c'est à vous de compléter :) Et si le fantôme n'est pas en état freight alors deux autre cas sont possibles. Soit la pacman respawn (s'est déjà fait tué) alors dans ce cas il a un état "SPAWN" qui lui permet d'être invulnérable lors de son respawn ! (pendant 2 secondes environ), s'il n'est pas dans cet état alors pacman meurt et perd une vie :( .
