import pygame
from pygame.locals import *
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from ghosts import GhostGroup
from pauser import Pauser
from levels import LevelController
from fruit import Fruit
from text import TextGroup
from sprites import Spritesheet
from maze import Maze

class GameController(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None
        self.background_flash = None
        self.setBackground()
        self.clock = pygame.time.Clock()
        self.pelletsEaten = 0
        self.pause = Pauser(True)
        self.fruit = None
        self.level = LevelController()
        self.text = TextGroup()
        self.score = 0
        self.gameover = False
        self.sheet = Spritesheet()
        self.maze = Maze(self.sheet)
        self.flashBackground = False
        self.eat_sound = pygame.mixer.Sound("./sound/pacman_chomp.wav")
        self.death_sound= pygame.mixer.Sound("./sound/pacman_death.wav")
        self.eatghost_sound= pygame.mixer.Sound("./sound/pacman_eatghost.wav")
        self.intro_sound=pygame.mixer.Sound("./sound/pacman_beginning.wav")
        self.intermission_sound=pygame.mixer.Sound("./sound/pacman_intermission.wav")
        
    def setBackground(self):
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_flash = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)

    def startGame(self):
        print("Start game")
        pygame.mixer.Sound.play(self.intro_sound)
        self.level.reset()
        levelmap = self.level.getLevel()
        self.maze.getMaze(levelmap["name"].split(".")[0])
        self.maze.constructMaze(self.background, self.background_flash, levelmap["row"])
        self.nodes = NodeGroup(levelmap["name"])
        self.pellets = PelletGroup(levelmap["name"])
        self.pacman = Pacman(self.nodes, self.sheet)
        self.ghosts = GhostGroup(self.nodes, self.sheet)
        self.pelletsEaten = 0
        self.fruit = None
        self.pause.force(True)
        self.text.showReady()
        self.text.updateLevel(self.level.level+1)
        self.gameover = False
        self.maze.reset()
        self.flashBackground = False
        
    def startLevel(self):
        print("Start new level")
        levelmap = self.level.getLevel()
        self.setBackground()
        self.maze.getMaze(levelmap["name"].split(".")[0])
        self.maze.constructMaze(self.background, self.background_flash, levelmap["row"])
        self.nodes = NodeGroup(levelmap["name"])
        self.pellets = PelletGroup(levelmap["name"])
        self.pacman.nodes = self.nodes
        self.pacman.reset()
        self.ghosts = GhostGroup(self.nodes, self.sheet)
        self.pelletsEaten = 0
        self.pause.force(True)
        self.fruit = None
        self.text.updateLevel(self.level.level+1)
        self.flashBackground = False
        self.maze.reset()
        
    def restartLevel(self):
        print("Restart current level")
        self.pacman.reset()
        self.ghosts = GhostGroup(self.nodes, self.sheet)
        self.pause.force(True)
        self.fruit = None
        self.flashBackground = False
        self.maze.reset()
        
    def update(self):
        if not self.gameover:
            dt = self.clock.tick(30) / 1000.0
            if not self.pause.paused:
                self.pacman.update(dt)
                self.ghosts.update(dt,self.pacman,self.ghosts.ghosts[0])
                
                if self.fruit is not None:
                    self.fruit.update(dt)

                if self.pause.pauseType != None:
                    self.pause.settlePause(self)
            
                self.checkPelletEvents()
                self.checkGhostEvents()
                self.checkFruitEvents()

            else:
                if self.flashBackground:
                    self.maze.flash(dt)
                    
                if self.pacman.animateDeath:
                    self.pacman.updateDeath(dt)

            self.pause.update(dt)
            self.pellets.update(dt)
            self.text.update(dt)
        self.checkEvents()
        self.text.updateScore(self.score)
        self.render()

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if self.gameover:
                        self.startGame()
                    else:
                        pygame.mixer.Sound.stop(self.intro_sound)
                        self.pause.player()
                        if self.pause.paused:
                            self.text.showPause()
                        else:
                            self.text.hideMessages()

    def checkFruitEvents(self):
        if self.fruit is not None:
            if self.pacman.eatFruit(self.fruit):
                self.score += self.fruit.points 
                self.text.createTemp(self.fruit.points, self.fruit.position)
                self.fruit = None
                
            elif self.fruit.destroy:
                self.fruit = None
        
    def checkPelletEvents(self):
        pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if(self.ghosts.isInFreightMode() and pygame.mixer.get_busy()==False):
            pygame.mixer.Sound.play(self.intermission_sound,loops=-1)
        elif (self.ghosts.isInFreightMode()==False):
            pygame.mixer.Sound.stop(self.intermission_sound)
        if pellet:
            pygame.mixer.Sound.play(self.eat_sound)
            self.pelletsEaten += 1
            self.score += pellet.points
            if (self.pelletsEaten == 70 or self.pelletsEaten == 140):
                if self.fruit is None:
                    levelmap = self.level.getLevel()
                    self.fruit = Fruit(self.nodes, self.sheet, levelmap["fruit"])
            self.pellets.pelletList.remove(pellet)
            if pellet.name == "powerpellet":
                pygame.mixer.Sound.stop(self.intermission_sound)
                pygame.mixer.Sound.play(self.intermission_sound,loops=-1)
                self.ghosts.resetPoints()
                self.ghosts.freightMode()
            if self.pellets.isEmpty():
                self.pacman.visible = False
                self.ghosts.hide()
                self.pause.startTimer(3, "clear")
                self.flashBackground = True
                

    def checkGhostEvents(self):
        self.ghosts.release(self.pelletsEaten)
        ghost = self.pacman.eatGhost(self.ghosts)
        if ghost is not None:
            if ghost.mode.name == "FREIGHT":
                pygame.mixer.Sound.play(self.eatghost_sound)
                self.score += ghost.points
                self.text.createTemp(ghost.points, ghost.position)
                self.ghosts.updatePoints()
                ghost.spawnMode(speed=2)
                self.pause.startTimer(1)
                self.pacman.visible = False
                ghost.visible = False
            
            elif ghost.mode.name != "SPAWN":
                pygame.mixer.Sound.play(self.death_sound)
                self.pacman.loseLife()
                self.ghosts.hide()
                self.pause.startTimer(3, "die")
            

    def resolveDeath(self):
        if self.pacman.lives == 0:
            self.gameover = True
            self.pacman.visible = False
            self.text.showGameOver()
        else:
            self.restartLevel()
        self.pause.pauseType = None
    
    def render(self):
        self.screen.blit(self.maze.background, (0,0))
        #self.nodes.render(self.screen)
        self.pellets.render(self.screen)
        if self.fruit is not None:
            self.fruit.render(self.screen)
        self.pacman.render(self.screen)
        self.ghosts.render(self.screen)
        self.pacman.renderLives(self.screen)
        self.text.render(self.screen)
        pygame.display.update()


if __name__ == "__main__":
    game = GameController()
    game.startGame()
    while True:
        game.update()
