import pygame
from entity import MazeRunner
from constants import *
from vector import Vector2
from modes import Mode
from random import randint
from stack import Stack
from animation import Animation

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
        self.animation = None
        self.animations = {}
        
    def findStartNode(self):
        for node in self.nodes.homeList:
            if node.homeEntrance:
                return node
        return node
    
    def spawnGoal(self):
        self.goal = self.spawnNode.position
    
    def spawnMode(self, speed=1):
        self.mode = Mode("SPAWN", speedMult=speed)
        self.setStartPosition()

    def findSpawnNode(self):
        for node in self.nodes.homeList:
            if node.spawnNode:
                break
        return node
    
    def freightMode(self):
        self.mode = Mode("FREIGHT", time=7, speedMult=0.5)
        self.modeTimer = 0

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

    def defineAnimations(self, row):
        anim = Animation("loop")
        anim.speed = 10
        anim.addFrame(self.spritesheet.getImage(0, row, TILEWIDTH*2, TILEHEIGHT*2))
        anim.addFrame(self.spritesheet.getImage(1, row, TILEWIDTH*2, TILEHEIGHT*2))
        self.animations["up"] = anim

        anim = Animation("loop")
        anim.speed = 10
        anim.addFrame(self.spritesheet.getImage(2, row, TILEWIDTH*2, TILEHEIGHT*2))
        anim.addFrame(self.spritesheet.getImage(3, row, TILEWIDTH*2, TILEHEIGHT*2))
        self.animations["down"] = anim

        anim = Animation("loop")
        anim.speed = 10
        anim.addFrame(self.spritesheet.getImage(4, row, TILEWIDTH*2, TILEHEIGHT*2))
        anim.addFrame(self.spritesheet.getImage(5, row, TILEWIDTH*2, TILEHEIGHT*2))
        self.animations["left"] = anim

        anim = Animation("loop")
        anim.speed = 10
        anim.addFrame(self.spritesheet.getImage(6, row, TILEWIDTH*2, TILEHEIGHT*2))
        anim.addFrame(self.spritesheet.getImage(7, row, TILEWIDTH*2, TILEHEIGHT*2))
        self.animations["right"] = anim

        anim = Animation("loop")
        anim.speed = 10
        anim.addFrame(self.spritesheet.getImage(0, 6, TILEWIDTH*2, TILEHEIGHT*2))
        anim.addFrame(self.spritesheet.getImage(1, 6, TILEWIDTH*2, TILEHEIGHT*2))
        self.animations["freight"] = anim

        anim = Animation("loop")
        anim.speed = 10
        anim.addFrame(self.spritesheet.getImage(0, 6, TILEWIDTH*2, TILEHEIGHT*2))
        anim.addFrame(self.spritesheet.getImage(2, 6, TILEWIDTH*2, TILEHEIGHT*2))
        anim.addFrame(self.spritesheet.getImage(1, 6, TILEWIDTH*2, TILEHEIGHT*2))
        anim.addFrame(self.spritesheet.getImage(3, 6, TILEWIDTH*2, TILEHEIGHT*2))
        self.animations["flash"] = anim

        anim = Animation("static")
        anim.speed = 10
        anim.addFrame(self.spritesheet.getImage(4, 6, TILEWIDTH*2, TILEHEIGHT*2))
        self.animations["spawnup"] = anim

        anim = Animation("static")
        anim.speed = 10
        anim.addFrame(self.spritesheet.getImage(5, 6, TILEWIDTH*2, TILEHEIGHT*2))
        self.animations["spawndown"] = anim

        anim = Animation("static")
        anim.speed = 10
        anim.addFrame(self.spritesheet.getImage(6, 6, TILEWIDTH*2, TILEHEIGHT*2))
        self.animations["spawnleft"] = anim

        anim = Animation("static")
        anim.speed = 10
        anim.addFrame(self.spritesheet.getImage(7, 6, TILEWIDTH*2, TILEHEIGHT*2))
        self.animations["spawnright"] = anim

    def updateAnimation(self, dt):
        if self.mode.name == "SPAWN":
            if self.direction == UP:
                self.animation = self.animations["spawnup"]
            elif self.direction == DOWN:
                self.animation = self.animations["spawndown"]
            elif self.direction == LEFT:
                self.animation = self.animations["spawnleft"]
            elif self.direction == RIGHT:
                self.animation = self.animations["spawnright"]
                
        if self.mode.name in ["CHASE", "SCATTER"]:
            if self.direction == UP:
                self.animation = self.animations["up"]
            elif self.direction == DOWN:
                self.animation = self.animations["down"]
            elif self.direction == LEFT:
                self.animation = self.animations["left"]
            elif self.direction == RIGHT:
                self.animation = self.animations["right"]
                
        if self.mode.name == "FREIGHT":
            if self.modeTimer >= (self.mode.time * 0.7):
                self.animation = self.animations["flash"]
            else:
                self.animation = self.animations["freight"]
        self.image = self.animation.update(dt)
    
    
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
                if key != self.direction * -1:
                    if not self.mode.name == "SPAWN":
                        if not self.node.homeEntrance:
                            if key not in self.bannedDirections:
                                validDirections.append(key)
                        else:
                            if key != DOWN:
                                validDirections.append(key)
                    else:
                        validDirections.append(key)
        if len(validDirections) == 0:
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
        
        self.updateAnimation(dt)

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
        self.defineAnimations(2)
        self.animation = self.animations["left"]

    def setStartPosition(self):
        ## Changement de la position de départ pour éviter que blinky se retrouve coincé dans la maison 
        self.setPosition()


    def moveBySelf(self):
        if self.overshotTarget():
            self.node = self.target
            validDirections = self.getValidDirections()
            ## On prend la direction la plus proche de pacman en la calculant selon la position de pacman
            self.direction = self.getClosestDirection(validDirections)
            self.target = self.node.neighbors[self.direction]
            self.setPosition()

    def update(self, dt,pacman):
        super().update(dt)
        self.mode.time=8
        if self.mode.name == "CHASE":
            self.chaseGoal(pacman)
        elif self.mode.name == "FREIGHT":
            self.randomGoal()
        elif self.mode.name == "SPAWN":
            self.spawnGoal()
        else:
            self.randomGoal()
        self.moveBySelf()

    def chaseGoal(self, pacman):
        self.goal= pacman.position

class Pinky(Ghost):
    def __init__(self, nodes, spritesheet):
        Ghost.__init__(self, nodes, spritesheet)
        self.name = "pinky"
        self.color = PINK
        self.image = self.spritesheet.getImage(0,3,TILEWIDTH*2, TILEHEIGHT*2)
        self.defineAnimations(3)
        self.animation = self.animations["up"]

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
        elif self.mode.name == "FREIGHT":
            self.randomGoal()
        elif self.mode.name == "SPAWN":
            self.spawnGoal()
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
        self.defineAnimations(4)
        self.animation = self.animations["down"]

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
        elif self.mode.name == "FREIGHT":
            self.randomGoal()
        elif self.mode.name == "SPAWN":
            self.spawnGoal()
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
        self.defineAnimations(5)
        self.animation = self.animations["down"]

    def setStartPosition(self):
        startNode = self.findStartNode()
        self.node = startNode.neighbors[DOWN].neighbors[UP].neighbors[LEFT].neighbors[LEFT].neighbors[DOWN]
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
        elif self.mode.name == "FREIGHT":
            self.randomGoal()
        elif self.mode.name == "SPAWN":
            self.spawnGoal()
        else:
            self.randomGoal()
        self.moveBySelf()

        
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
                    ghost.spawnMode()
                    ghost.released = True
    
    def freightMode(self):
        for ghost in self:
            ghost.freightMode()

    def isInFreightMode(self):
        for ghost in self:
            if(ghost.mode.name=="FREIGHT"):
                return True
        return False

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
            
