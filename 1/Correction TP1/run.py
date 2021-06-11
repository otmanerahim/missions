import pygame
from pygame.locals import *
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from ghosts import GhostGroup
from sprites import Spritesheet
from pellets import PelletGroup
from maze import Maze

class GameController(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None
        self.background_flash = None
        self.setBackground()
        self.clock = pygame.time.Clock()
        self.sheet = Spritesheet()
        self.maze = Maze(self.sheet)
        
    def setBackground(self):
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_flash = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)

    def startGame(self):

        ## Création de la map ##
        self.maze.getMaze("maze1")
        self.maze.constructMaze(self.background, self.background_flash, 0)
        self.nodes = NodeGroup("maze1.txt")
        self.pellets = PelletGroup("pellets1.txt")
        self.pacman = Pacman(self.nodes, self.sheet)
        self.ghosts = GhostGroup(self.nodes, self.sheet)
        self.maze.reset()
        self.flashBackground = False
        
        
    def update(self):
        dt = self.clock.tick(30) / 1000.0
        self.pacman.update(dt)
        self.ghosts.update(dt,self.pacman)
        
        self.pellets.update(dt)
        self.checkPelletEvents()
        self.checkEvents()
        self.render()
        
    def checkPelletEvents(self):
        pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if pellet:
            self.pellets.pelletList.remove(pellet)
    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

    def render(self):
        self.screen.blit(self.maze.background, (0,0))
        self.pacman.render(self.screen)
    
        self.pellets.render(self.screen)
        self.ghosts.render(self.screen)
        pygame.display.update()


if __name__ == "__main__":
    game = GameController()
    game.startGame()
    while True:
        game.update()
