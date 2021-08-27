# TP7

Pour se rapprocher de pacman original, on va copier le mouvement de "scatter" dans lequel les fantômes du jeu "patrouillent" dans un coin de l'écran

Jusqu'à maintenant les fantômes prenaient une position aléatoire pour pattrouilaient, maintenant chaque fantôme va patrouiller dans un coin de l'écran lorsque celui-ci sera en état "scatter".

Pour ce faire, je pense que vous l'aurez compris il faudra changer le code qui se trouve ci-dessous

```py
def update(self, dt,pacman):
       super().update(dt)
       self.mode.time=10
       if self.mode.name == "CHASE":
           self.chaseGoal(pacman)
       elif self.mode.name == "FREIGHT":
           self.randomGoal()
       elif self.mode.name == "SPAWN":
           self.spawnGoal()

       elif self.mode.name == "SCATTER":
           self.scatterGoal()
       else:
           self.randomGoal()
       self.moveBySelf()
```

La fonction scatterGoal sera à completer !
