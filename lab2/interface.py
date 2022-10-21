import time
import sys

import pygame as pg
import numpy as np

from player import Player
from logger import Logger
from warhol import Warhol

class Interface():
    def __init__(self,
                WINDOW_HEIGHT=400,
                WINDOWS_WIDTH=400,
                BLOCKSIZE=20,
                NUM_PLAYERS_PER_TEAM=5,
                NUM_OBSTACLES=5):

        self.BLOCKSIZE=BLOCKSIZE
        self.WINDOW_HEIGHT=WINDOW_HEIGHT+self.BLOCKSIZE
        self.WINDOW_WIDTH=WINDOWS_WIDTH+self.BLOCKSIZE
        self.NUM_PLAYERS_PER_TEAM=NUM_PLAYERS_PER_TEAM
        self.NUM_PLAYERS_ALIVE = NUM_PLAYERS_PER_TEAM*2

        self.SCREEN = pg.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.CLOCK = pg.time.Clock()
        pg.display.set_caption("Panico Game")
        icon=pg.image.load("logo.jpg")
        pg.display.set_icon(icon)

        self.SPAWN_OFFSET = self.BLOCKSIZE*5
        self.SPAWN_POSITIONS_TEAM_1 = [(i*self.SPAWN_OFFSET, 0) for i in range(self.NUM_PLAYERS_PER_TEAM)]
        self.SPAWN_POSITIONS_TEAM_2 = [(i*self.SPAWN_OFFSET, self.WINDOW_HEIGHT-self.BLOCKSIZE) for i in range(self.NUM_PLAYERS_PER_TEAM)]

        self.TEAM1 = [Player(tag=f"p{i}_t1", spawnPosition=self.SPAWN_POSITIONS_TEAM_1[i]) for i in range(self.NUM_PLAYERS_PER_TEAM)]
        self.TEAM2 = [Player(tag=f"p{i}_t2", spawnPosition=self.SPAWN_POSITIONS_TEAM_2[i]) for i in range(self.NUM_PLAYERS_PER_TEAM)]

        self.NUM_OBSTACLES = NUM_OBSTACLES
        self.OBSTACLES_POSITIONS = [(260, 260), (200, 180), (140, 240), (100, 160), (170, 340)]

    def designInterface(self):
        for x in range(0, self.WINDOW_WIDTH, self.BLOCKSIZE):
            for y in range(0, self.WINDOW_HEIGHT, self.BLOCKSIZE):
                gridElement = pg.Rect(x, y, self.BLOCKSIZE, self.BLOCKSIZE)
                pg.draw.rect(self.SCREEN, (200, 200, 200), gridElement, 1)

    def spawnPlayers(self):
        for coordinates in self.SPAWN_POSITIONS_TEAM_1:
            pg.draw.rect(self.SCREEN, (200, 200, 200), pg.Rect(coordinates[0], coordinates[1], self.BLOCKSIZE, self.BLOCKSIZE), 0)
        for coordinates in self.SPAWN_POSITIONS_TEAM_2:
            pg.draw.rect(self.SCREEN, (200, 200, 200), pg.Rect(coordinates[0], coordinates[1], self.BLOCKSIZE, self.BLOCKSIZE), 0)

    def spawnMovedPlayers(self):
        for player in self.TEAM1:
            pg.draw.rect(self.SCREEN, (200, 200, 200), pg.Rect(player.position[0], player.position[1], self.BLOCKSIZE, self.BLOCKSIZE), 0)
        for player in self.TEAM2:
            pg.draw.rect(self.SCREEN, (200, 200, 200), pg.Rect(player.position[0], player.position[1], self.BLOCKSIZE, self.BLOCKSIZE), 0)

    def spawnObstacles(self):
        for coordinates in self.OBSTACLES_POSITIONS:
            pg.draw.rect(self.SCREEN, (255, 0, 0), pg.Rect(coordinates[0], coordinates[1], self.BLOCKSIZE, self.BLOCKSIZE), 0)

    def interfaceSetup(self):
        self.designInterface()
        self.spawnPlayers()
        self.spawnObstacles()

    def clean_interface(self):
        self.SCREEN.fill((0, 0, 0))
        self.designInterface()

    def movePlayers(self):
        for player in self.TEAM1:
            pass
        for player in self.TEAM2:
            pass

    def resolveBattles(self):
        pass

    def drawNewInterface(self):
        self.designInterface()
        self.spawnMovedPlayers()
        self.spawnObstacles()


    def startGame(self):
        pg.init()

        self.SCREEN.fill((0, 0, 0))#filling the screen with black
        
        self.interfaceSetup()
        #self.debug()
        
        while True:
            self.movePlayers()
            self.resolveBattles()
            self.clean_interface()
            self.drawNewInterface()
            for e in pg.event.get():
                if e.type==pg.QUIT:
                    pg.quit()
                    sys.exit()
            time.sleep(.5)
            pg.display.update()

    def debug(self):
        pass