import pygame
from entity import MazeRunner
from constants import *
from vector import Vector2
from random import randint
from stack import Stack

class Ghost(MazeRunner):
    def __init__(self, nodes, spritesheet):
        MazeRunner.__init__(self, nodes, spritesheet)
        self.name = "ghost"

        ## Permet de définir l'objectif de l'IA, c'est une position vectorielle qui pourra être modifié
        ## pour prendre en compte la position de pacman par exemple... ;)
        self.goal = Vector2()

        ## Permet de définir où vont apparaitre les fantômes après leur mort ou au début du jeu 
        self.spawnNode = self.findSpawnNode()
        self.pelletsForRelease = 0
        self.released = True
        self.bannedDirections = []
        self.setStartPosition()
        self.points = 200
    

    ## Fonction permettant de définir le premier noeud où vont apparaitre les personnages du jeu
    def findStartNode(self):
        for node in self.nodes.homeList:
            if node.homeEntrance:
                return node
        return node

    ## Cette fonction est à compléter, cela permet de calculer la direction la plus courte pour atteindre
    ## un objectif nommé "goal"
    def getClosestDirection(self, validDirections):
        
    
    def setStartPosition(self):
        self.node = self.findStartNode()
        self.target = self.node
        self.setPosition()
        
    ## Fonction permettant de trouver une direction valide (trouver un noeud voisin)
    ## Un noeud voisin est le premier noeud qui peut être à droite, à gauche, en haut ou en bas du personnage
    def getValidDirections(self):
        validDirections = []
        for key in self.node.neighbors.keys():
            if self.node.neighbors[key] is not None:
                validDirections.append(key)
        return validDirections
    
    ## Fonction choisissant une direction aléatoire parmi les directions valides
    def randomDirection(self, validDirections):
        index = randint(0, len(validDirections) - 1)
        return validDirections[index]

    ## Fonction du jeu permettant de faire avancer la position d'un personnage du jeu en attribuant une nouvelle position
    def moveBySelf(self):
        if self.overshotTarget():
            self.node = self.target
            validDirections = self.getValidDirections()
            self.direction = self.randomDirection(validDirections)
            self.target = self.node.neighbors[self.direction]
            self.setPosition()
    
    ## Fonction du jeu calculant la nouvelle position d'un personnage en fonction de sa direction et de sa vitesse
    def update(self, dt):
        self.visible = True
        self.position += self.direction*self.speed*dt
        self.moveBySelf()

    ## Fonction du jeu permettant de réduire la vitesse d'un personnage lorsqu'il passe le portail
    def portalSlowdown(self):
        self.speed = 100
        if self.node.portalNode or self.target.portalNode:
            self.speed = 50

    ## Fonction du jeu retournant un objectif aléatoire, l'objectif est un vecteur
    def randomGoal(self):
        x = randint(0, NCOLS*TILEWIDTH)
        y = randint(0, NROWS*TILEHEIGHT)
        self.goal = Vector2(x, y)

    ## Fonction du jeu permettant de trouver le point de départ d'un personnage
    def findSpawnNode(self):
        for node in self.nodes.homeList:
            if node.spawnNode:
                break
        return node

    ## Fonction du jeu permettant de définir le point de départ d'un personnage lors de sa mort 
    def spawnGoal(self):
        self.goal = self.spawnNode.position


class Blinky(Ghost):
    def __init__(self, nodes, spritesheet):
        Ghost.__init__(self, nodes, spritesheet)
        self.name = "blinky"
        self.color = RED
        self.image = self.spritesheet.getImage(4,2,TILEWIDTH*2, TILEHEIGHT*2)

    def setStartPosition(self):
        ## Changement de la position de départ pour éviter que blinky se retrouve coincé dans la maison 
        self.setPosition()

    # def getValidDirections(self,pacman):

    # def moveBySelf(self,pacman):

    # def update(self, dt,pacman):
        
    # def chaseGoal(self, pacman):

class Pinky(Ghost):
    def __init__(self, nodes, spritesheet):
        Ghost.__init__(self, nodes, spritesheet)
        self.name = "pinky"
        self.color = PINK
        self.image = self.spritesheet.getImage(0,3,TILEWIDTH*2, TILEHEIGHT*2)

    def setStartPosition(self):
        startNode = self.findStartNode()
        self.node = startNode.neighbors[DOWN]
        self.target = self.node
        self.setPosition()
        

class Inky(Ghost):
    def __init__(self, nodes, spritesheet):
        Ghost.__init__(self, nodes, spritesheet)
        self.name = "inky"
        self.color = TEAL
        self.pelletsForRelease = 30
        self.released = False
        self.image = self.spritesheet.getImage(2,4,TILEWIDTH*2, TILEHEIGHT*2)


    def setStartPosition(self):
        self.bannedDirections = [RIGHT]
        startNode = self.findStartNode()
        pinkyNode = startNode.neighbors[DOWN]
        self.node = pinkyNode.neighbors[LEFT]
        self.target = self.node
        self.spawnNode = pinkyNode.neighbors[LEFT]
        self.setPosition()
        

        
        
class Clyde(Ghost):
    def __init__(self, nodes, spritesheet):
        Ghost.__init__(self, nodes, spritesheet)
        self.name = "clyde"
        self.color = ORANGE
        self.pelletsForRelease = 60
        self.released = False
        self.image = self.spritesheet.getImage(2,5,TILEWIDTH*2, TILEHEIGHT*2)

    def setStartPosition(self):
        self.bannedDirections = [LEFT]
        startNode = self.findStartNode()
        pinkyNode = startNode.neighbors[DOWN]
        self.node = pinkyNode.neighbors[RIGHT]
        self.spawnNode = pinkyNode.neighbors[RIGHT]
        self.target = self.node
        self.setPosition()
        

        
class GhostGroup(object):
    def __init__(self, nodes, spritesheet):
        self.nodes = nodes
        self.ghosts = [Blinky(nodes, spritesheet),
                       Pinky(nodes, spritesheet),
                       Inky(nodes, spritesheet),
                       Clyde(nodes, spritesheet)]
        
    def __iter__(self):
        return iter(self.ghosts)

    def update(self, dt):
        for ghost in self:
            ghost.update(dt)
            

    def release(self, numPelletsEaten):
        for ghost in self:
            if not ghost.released:
                if numPelletsEaten >= ghost.pelletsForRelease:
                    ghost.bannedDirections = []
                    ghost.released = True

    def updatePoints(self):
        for ghost in self:
            ghost.points *= 2

    def resetPoints(self):
        for ghost in self:
            ghost.points = 200

    def hide(self):
        for ghost in self:
            ghost.visible = False
            
    def render(self, screen):
        for ghost in self:
            ghost.render(screen)
            
