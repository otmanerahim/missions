import pygame
from entity import MazeRunner
from constants import *
from vector import Vector2
from modes import Mode
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
        self.modeStack = self.setupModeStack()
        self.mode = self.modeStack.pop()
        self.modeTimer = 0
        
    def findStartNode(self):
        for node in self.nodes.homeList:
            if node.homeEntrance:
                return node
        return node
        
    def setupModeStack(self):
        modes = Stack()
        modes.push(Mode(name="CHASE"))
        modes.push(Mode(name="SCATTER"))
        modes.push(Mode(name="CHASE"))
        modes.push(Mode(name="SCATTER"))
        modes.push(Mode(name="CHASE"))
        modes.push(Mode(name="SCATTER"))
        modes.push(Mode(name="CHASE"))
        modes.push(Mode(name="SCATTER"))
        return modes
    
    
    def forceBacktrack(self):
        if self.direction * -1 == UP:
            return UP
        if self.direction * -1 == DOWN:
            return DOWN
        if self.direction * -1 == LEFT:
            return LEFT
        if self.direction * -1 == RIGHT:
            return RIGHT
    
    
    def modeUpdate(self, dt):
        self.modeTimer += dt
        if self.mode.time is not None:
            if self.modeTimer >= self.mode.time:
                self.mode = self.modeStack.pop()
                self.modeTimer = 0
    
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
        if (len(validDirections) == 0):
            validDirections.append(self.forceBacktrack())
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
        self.modeUpdate(dt)
        print("Actual mode for ", self.name , " : ", self.mode.name , " : ", self.mode.time)

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
       if (len(validDirections) == 0):
            validDirections.append(self.forceBacktrack())
       return validDirections


    def moveBySelf(self,pacman):
        if self.overshotTarget():
            self.node = self.target
            validDirections = self.getValidDirections(pacman)
            ## On prend la direction la plus proche de pacman en la calculant selon la position de pacman
            self.direction = self.getClosestDirection(validDirections)
            self.target = self.node.neighbors[self.direction]
            self.setPosition()

    def update(self, dt,pacman):
        super().update(dt)
        self.mode.time=8
        if self.mode.name == "CHASE":
            self.chaseGoal(pacman)
        else:
            self.randomGoal()
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
        self.node = startNode.neighbors[DOWN].neighbors[UP].neighbors[RIGHT].neighbors[RIGHT]
        self.target = self.node
        self.setPosition()

    def moveBySelf(self):
        if self.overshotTarget():
            self.node = self.target
            validDirections = self.getValidDirections()
            self.direction = self.getClosestDirection(validDirections)
            self.target = self.node.neighbors[self.direction]
            self.setPosition()
    
    def chaseGoal(self, pacman):
        self.goal =pacman.position+ pacman.direction * TILEWIDTH * 4

    def update(self, dt,pacman):
        super().update(dt)
        self.mode.time=12
        if self.mode.name == "CHASE":
            self.chaseGoal(pacman)
        else:
            self.randomGoal()
        self.moveBySelf()
        

class Inky(Ghost):
    def __init__(self, nodes, spritesheet):
        Ghost.__init__(self, nodes, spritesheet)
        self.name = "inky"
        self.color = TEAL
        self.pelletsForRelease = 30
        self.released = False
        self.image = self.spritesheet.getImage(2,4,TILEWIDTH*2, TILEHEIGHT*2)


    def setStartPosition(self):
        startNode = self.findStartNode()
        self.node = startNode.neighbors[DOWN].neighbors[UP].neighbors[LEFT].neighbors[LEFT]
        self.target = self.node
        self.setPosition()

    def moveBySelf(self):
        if self.overshotTarget():
            self.node = self.target
            self.portal()
            validDirections = self.getValidDirections()
            self.direction = self.getClosestDirection(validDirections)
            self.target = self.node.neighbors[self.direction]
            self.setPosition()

    def chaseGoal(self, pacman, blinky):
        vec1 = pacman.position + pacman.direction * TILEWIDTH * 2
        vec2 = (vec1 - blinky.position) * 2
        self.goal = blinky.position + vec2
        
    def update(self, dt,pacman,blinky):
        super().update(dt)
        self.mode.time=15
        if self.mode.name == "CHASE":
            self.chaseGoal(pacman,blinky)
        else:
            self.randomGoal()
        self.moveBySelf()
        

        
        
class Clyde(Ghost):
    def __init__(self, nodes, spritesheet):
        Ghost.__init__(self, nodes, spritesheet)
        self.name = "clyde"
        self.color = ORANGE
        self.pelletsForRelease = 60
        self.released = False
        self.image = self.spritesheet.getImage(2,5,TILEWIDTH*2, TILEHEIGHT*2)

    def setStartPosition(self):
        startNode = self.findStartNode()
        self.node = startNode.neighbors[DOWN].neighbors[UP].neighbors[LEFT].neighbors[LEFT].neighbors[DOWN]
        self.target = self.node
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
            self.portal()
            validDirections = self.getValidDirections(pacman)
            self.direction = self.getClosestDirection(validDirections)
            self.target = self.node.neighbors[self.direction]
            self.setPosition()
            
    
    def chaseGoal(self, pacman):
        d = pacman.position - self.position
        ds = d.magnitudeSquared()
        if ds <= (TILEWIDTH * 8)**2:
            self.goal = self.randomDirection(super().getValidDirections()) * TILEWIDTH
        else:
            self.goal = pacman.position + pacman.direction * TILEWIDTH * 4
    
    def update(self, dt,pacman):
        super().update(dt)
        self.mode.time=10
        if self.mode.name == "CHASE":
            self.chaseGoal(pacman)
        else:
            self.randomGoal()
        self.moveBySelf(pacman)

        
class GhostGroup(object):
    def __init__(self, nodes, spritesheet):
        self.nodes = nodes
        self.ghosts = [Blinky(nodes, spritesheet),
                       Pinky(nodes, spritesheet),
                       Inky(nodes, spritesheet),
                       Clyde(nodes, spritesheet)]
        
    def __iter__(self):
        return iter(self.ghosts)

    def update(self, dt,pacman,blinky=None):
        for ghost in self:
            if(ghost.name=="blinky" or ghost.name=="pinky" or ghost.name=="clyde"):
                ghost.update(dt,pacman)
            elif(ghost.name=="inky"):
                ghost.update(dt,pacman,blinky)
            

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
            
