# TP1

Durant cette première partie de TP il vous faudra changez le comportement de Blinky pour qu'il aille dans la direction de pac-man (sans jamais faire machine arrière). A chaque fois qu'il arrive à une intersection, il choisit celle qui correspond le plus à la direction de pacman (sauf faire demi-tour).

Afin de réaliser le premier TP je vais vous donner un premier coup de pouce en vous indiquant les fonctions clés qui sont utilisés pour gérer le déplacement des personnages ! :)

Ces fonctions peuvent être retrouvés dans le fichier ghosts.py !

```py
def getValidDirections(self):
        validDirections = []
        for key in self.node.neighbors.keys():
            if self.node.neighbors[key] is not None:
                validDirections.append(key)
        return validDirections
```

Cette fonction permet de retourner une direction valide à un personnage du jeu ! Mais vous vous dites sûrement ce que je veux dire par valide n'est-ce pas ? Alors je vais vous dire un secret pour vous aider dans la compréhension de ce jeu ! Comme vous avez pu le remarquer dans la fonction on voit apparaitre **"node"**, **"neighbours"**. Si vous êtes familier avec les graphes c'est une bonne nouvelle, car la map est en faites... un graphe ! Avec une image cela sera beaucoup plus clair !

![Foo](https://img1.wsimg.com/isteam/ip/51f9eb68-183a-416f-aedc-5c476e4e4d1c/paused.png/:/cr=t:0%25,l:0%25,w:100%25,h:100%25/rs=w:400,cg:true)

Voilà l'envers du décor ! La carte de pacman est en faites composés de **noeuds**, et un **noeud voisin** est le noeud le plus proche d'un autre noeud (qui peut être à droite, à gauche, en haut ou en bas). Maintenant vous pouvez mieux comprendre la fonction qui cherche un noeud voisin, si un noeud voisin existe alors on retourne la ou **LES** directions qui permettent d'atteindre ce noeud ! Jusque là plutôt simple :)

```py
def update(self, dt):
        self.visible = True
        self.position += self.direction*self.speed*dt
        self.moveBySelf()
```

La deuxième fonction permet à un personnage du jeu de mettre à jour sa position en fonction de sa direction et de sa vitesse. **dt** ici représente le temps. Et je vais vous expliquer par la suite la fonction **moveBySelf**.

```py
 def moveBySelf(self):
        if self.overshotTarget():
            self.node = self.target
            validDirections = self.getValidDirections()
            self.direction = self.randomDirection(validDirections)
            self.target = self.node.neighbors[self.direction]
            self.setPosition()
```

On peut voir dans la première ligne une condition. Il n'y a pas besoin d'aller en détail dans cette fonction, il faut simplement comprendre que cette fonction permet de détecter si un personnage du jeu a dépassé son objectif ! Mais quel objectif ? Comme on a pu le voir la carte est composé de noeuds, chaque personnage se déplace s'il y a un noeud voisin, mais cela serait assez problématique si le personnage ne s'arrête pas en bout de course une fois qu'il a atteint un noeud voisin ! On pourrait arriver avec ce genre de problème...

![Foo](https://img1.wsimg.com/isteam/ip/51f9eb68-183a-416f-aedc-5c476e4e4d1c/node2part3.png/:/cr=t:0%25,l:0%25,w:100%25,h:100%25/rs=w:600,h:300,cg:true)

C'est pour cette raison qu'il faut toujours vérifier si un personnage a atteint un noeud, si oui alors recalcule sa position et on trouve le prochain noeud à atteindre ! On commence par trouver une direction valide, puis on la met en "**target**" ! Voilà j'espère que vous aurez mieux compris l'utilité de cette fonction !

Avant de vous laisser faire le TP, je voudrais aussi noté un dernier point très important !

```py
class Ghost(MazeRunner):
    def __init__(self, nodes, spritesheet):
        MazeRunner.__init__(self, nodes, spritesheet)
        self.name = "ghost"
        self.goal = Vector2()
```

Ici dans la classe Ghost il y a une variable nommé **"goal"**, il est important de comprendre l'utilité de cette variable qui représente ici un vecteur car vous devrez l'utiliser pour accomplir ce TP ! Chaque personnage du jeu a un **objectif** et les calculs seront réalisés à partir de cet objectif

```py
def randomDirection(self, validDirections):
        index = randint(0, len(validDirections) - 1)
        return validDirections[index]
```

Pour commencer le TP j'ai mis que tous les fantômes prennent une direction aléatoire, mais comme on veut changer le comportement de Blinky, il faudra ajouter une autre fonction qui permettra de calculer la direction à prendre selon **l'objectif de Blinky** !

```py
def getClosestDirection(self, validDirections):
       # à compléter
```

Ainsi vous trouverez dans le fichier ghosts.py une fonction incomplète que vous devrez remplir pour que Blinky puisse accomplir son objectif ;) Cette fonction retournera la direction la plus proche de notre objectif (qui sera pacman ;) )

Je pense que vous l'aurez compris comme on veut changer le comportement de Blinky, il faudra réécrire des fonctions parents afin de modifier son comportement de base, et j'ai ici ajouté les informations concernant pacman afin de pouvoir récupérer sa position ! A vous de jouer compléter les fonctions !

```py
class Blinky(Ghost):
    def __init__(self, nodes, spritesheet):
        Ghost.__init__(self, nodes, spritesheet)
        self.name = "blinky"
        self.color = RED
        self.image = self.spritesheet.getImage(4,2,TILEWIDTH*2, TILEHEIGHT*2)


    # def getValidDirections(self,pacman):

    # def moveBySelf(self,pacman):

    # def chaseGoal(self, pacman):

    # def update(self, dt,pacman):

```
