# TP5

Vous êtes maintenant arrivé au TP5 ! Durant ce TP nous allons complexifier un peu plus les différentes IA qu'on a créées en ajoutant des **états** (différent pour chaque fantôme) ! Si vous l'avez remarqué en jouant, les fantômes ne sont pas tout le temps en train de poursuivre pacman, il y a des moments où les fantômes ont d'autre objectifs afin de laisser le joueur souffler un peu ! Et dans le jeu les fantômes alterne entre plusieurs états, dans ce TP nous allons créer deux états **"Scatter"** et **"Chase"**.

Scatter est l'état où les fantômes ont pour objectif d'aller chacun dans leur coin respectif, cependant dans ce TP nous allons juste créer les états sans les comportements associés à cet état afin de rester simple pour l'instant ! Et ce que nous allons faire c'est alterner entre l'état "Scatter" et "Chase" avec pour chaque état un temps qui lui est associé. De plus les fantômes devront avoir chacun un timer différent.

Vous aurez ainsi une nouvelle classe classe qui représente un état !

```py
class Mode(object):
    def __init__(self, name="", time=None, speedMult=1, direction=None):
        self.name = name
        self.time = time
```

Il y'aura le nom de l'état et le temps !

De plus vous allez avoir deux nouvelles variables dans la classe Ghost qui seront déjà prédéfinie, cela servira à initialiser les états !

```py
class Ghost(MazeRunner):
    def __init__(self, nodes, spritesheet):
        self.modeStack = self.setupModeStack()
        self.mode = self.modeStack.pop()
```

Comme vous pouvez le voir ces deux variables ont pour structure de données une **"pile"** ! L'idée est simple, dans cette pile il y'aura nos différents états ! on met un timer pour chaque fantôme et quand le timer a été dépassé on dépile (on passe au prochain état) !

```py
def modeUpdate(self, dt):
   # A completer
```

Vous allez ainsi devoir compléter cette fonction qui servira à mettre à jour notre pile d'état !

Une fois cela fait vous devrez ajouter cette fonction dans la fonction update du jeu ci-dessous !

```py
def update(self, dt):
        self.modeUpdate(dt)
```

Et enfin il ne vous reste plus qu'à mettre un timer différent pour chaque fantôme :)
