
from entity import MazeRunner
from constants import *
from random import randint
from animation import Animation

class Ghost(MazeRunner):
    def __init__(self, nodes, spritesheet):
        MazeRunner.__init__(self, nodes, spritesheet)
        self.name = "ghost"
        self.goal = Vector2()
        self.setStartPosition()
        
    
    def setStartPosition(self):
        self.target = self.node
        self.setPosition()
        
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

    
    def getClosestDirection(self, validDirections):
        distances = []
        for direction in validDirections:
            diffVec = self.node.position + direction*TILEWIDTH - self.goal
            distances.append(diffVec.magnitudeSquared())
        index = distances.index(min(distances))
        return validDirections[index]
    
    def getDirectionPacMan(self,pacman):
        return pacman.direction

    
    def update(self, dt):
        self.visible = True
        self.position += self.direction*self.speed*dt
        self.moveBySelf()

        

class Blinky(Ghost):
    def __init__(self, nodes, spritesheet):
        Ghost.__init__(self, nodes, spritesheet)
        self.name = "blinky"
        self.color = RED
        self.image = self.spritesheet.getImage(4,2,TILEWIDTH*2, TILEHEIGHT*2)

    def getValidDirections(self,pacman):
        validDirections = []
        for key in self.node.neighbors.keys():
            if self.node.neighbors[key] is not None:
                if key != self.direction * -1:
                    validDirections.append(key)
        if(len(validDirections)==0):
            if key != self.direction * -1:
                validDirections.append(pacman.direction)
        return validDirections

    def moveBySelf(self,pacman):
        if self.overshotTarget():
            self.node = self.target
            validDirections = self.getValidDirections(pacman)
            self.direction = self.getClosestDirection(validDirections)
            self.target = self.node.neighbors[self.direction]
            self.setPosition()

    def update(self, dt,pacman):
        self.visible = True
        self.position += self.direction*self.speed*dt
        if(self.name=="blinky"):
            self.chaseGoal(pacman)
        self.moveBySelf(pacman)

    def chaseGoal(self, pacman):
        self.goal =pacman.position+ pacman.direction * TILEWIDTH

    

class Pinky(Ghost):
    def __init__(self, nodes, spritesheet):
        Ghost.__init__(self, nodes, spritesheet)
        self.name = "pinky"
        self.color = PINK
        self.image = self.spritesheet.getImage(0,3,TILEWIDTH*2, TILEHEIGHT*2)

    def setStartPosition(self):
        self.setPosition()
        

class Inky(Ghost):
    def __init__(self, nodes, spritesheet):
        Ghost.__init__(self, nodes, spritesheet)
        self.name = "inky"
        self.color = TEAL
        self.image = self.spritesheet.getImage(2,4,TILEWIDTH*2, TILEHEIGHT*2)

    def setStartPosition(self):
        self.setPosition()
        
        
        
class Clyde(Ghost):
    def __init__(self, nodes, spritesheet):
        Ghost.__init__(self, nodes, spritesheet)
        self.name = "clyde"
        self.color = ORANGE
        self.image = self.spritesheet.getImage(2,5,TILEWIDTH*2, TILEHEIGHT*2)
        
            
    def setStartPosition(self):
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
            
    def render(self, screen):
        for ghost in self:
            ghost.render(screen)
            