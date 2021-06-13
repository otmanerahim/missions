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
        self.goal = Vector2()
        self.spawnNode = self.findSpawnNode()
        self.pelletsForRelease = 0
        self.released = True
        self.bannedDirections = []
        self.setStartPosition()
        self.points = 200
        
    def findStartNode(self):
        for node in self.nodes.homeList:
            if node.homeEntrance:
                return node
        return node
    
    def setStartPosition(self):
        self.node = self.findStartNode()
        self.target = self.node
        self.setPosition()
        
    def getClosestDirection(self, validDirections):
        distances = []
        for direction in validDirections:
            diffVec = self.node.position + direction*TILEWIDTH - self.goal
            distances.append(diffVec.magnitudeSquared())
        index = distances.index(min(distances))
        return validDirections[index]
        
    def getValidDirections(self):
        validDirections = []
        for key in self.node.neighbors.keys():
            if self.node.neighbors[key] is not None:
                validDirections.append(key)
        return validDirections
    
    def randomDirection(self, validDirections):
        index = randint(0, len(validDirections) - 1)
        return validDirections[index]
    
    def moveBySelf(self):
        if self.overshotTarget():
            self.node = self.target
            validDirections = self.getValidDirections()
            self.direction = self.randomDirection(validDirections)
            self.target = self.node.neighbors[self.direction]
            self.setPosition()
    
                
    def update(self, dt):
        self.visible = True
        self.position += self.direction*self.speed*dt
        self.moveBySelf()

    def portalSlowdown(self):
        self.speed = 100
        if self.node.portalNode or self.target.portalNode:
            self.speed = 50


    def randomGoal(self):
        x = randint(0, NCOLS*TILEWIDTH)
        y = randint(0, NROWS*TILEHEIGHT)
        self.goal = Vector2(x, y)

        
    def findSpawnNode(self):
        for node in self.nodes.homeList:
            if node.spawnNode:
                break
        return node
    
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

    def getValidDirections(self,pacman):
       validDirections = []
       for key in self.node.neighbors.keys():
            if self.node.neighbors[key] is not None:
                if(key != self.direction * -1 ):
                    validDirections.append(key)
       return validDirections


    def moveBySelf(self,pacman):
        if self.overshotTarget():
            self.node = self.target
            validDirections = self.getValidDirections(pacman)
            ## On prend la direction la plus proche de pacman en la calculant selon la position de pacman
            self.direction = self.getClosestDirection(validDirections)
            print("#### Direction de Blinky : ", self.direction , "Direction de pacman : ",pacman.direction," ####")
            self.target = self.node.neighbors[self.direction]
            self.setPosition()

    def update(self, dt,pacman):
        self.visible = True
        self.position += self.direction*self.speed*dt
        self.chaseGoal(pacman)
        self.moveBySelf(pacman)

    def chaseGoal(self, pacman):
        self.goal= pacman.position

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

    def update(self, dt,pacman):
        for ghost in self:
            if(ghost.name=="blinky"):
                ghost.update(dt,pacman)
            else:
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
            
