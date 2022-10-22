import time
import sys

import pygame as pg
import numpy as np

from player import Player
from logger import Logger
from warhol import Warhol

class Interface():
    def __init__(self,
                WINDOW_HEIGHT=200,
                WINDOWS_WIDTH=200,
                BLOCKSIZE=20,
                NUM_PLAYERS_PER_TEAM=2,
                NUM_OBSTACLES=5,
                OBSTACLES=False):

        self.BLOCKSIZE=BLOCKSIZE
        self.WINDOW_HEIGHT=WINDOW_HEIGHT+self.BLOCKSIZE
        self.WINDOW_WIDTH=WINDOWS_WIDTH+self.BLOCKSIZE

        self.NORMALIZED_WINDOW_HEIGHT=self.WINDOW_HEIGHT-self.BLOCKSIZE
        self.NORMALIZED_WINDOW_WIDTH=self.WINDOW_WIDTH-self.BLOCKSIZE

        self.NUM_PLAYERS_PER_TEAM=NUM_PLAYERS_PER_TEAM
        self.NUM_PLAYERS_ALIVE = NUM_PLAYERS_PER_TEAM*2

        #CONFIGURATION OF GAME SESSION
        self.SCREEN = pg.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.CLOCK = pg.time.Clock()
        pg.display.set_caption("Panico Game")
        icon=pg.image.load("logo.jpg")
        pg.display.set_icon(icon)

        self.SPAWN_OFFSET = self.NORMALIZED_WINDOW_WIDTH/self.NUM_PLAYERS_PER_TEAM
        # adjust_offset = False
        # if self.SPAWN_OFFSET % self.BLOCKSIZE != 0:
        #     adjust_offset = True
        # while adjust_offset:
        #     self.SPAWN_OFFSET += 1
        #     if self.SPAWN_OFFSET % self.BLOCKSIZE == 0:
        #         adjust_offset = False

        self.SPAWN_POSITIONS_TEAM_1 = [(self.SPAWN_OFFSET+i*self.SPAWN_OFFSET, 0) for i in range(self.NUM_PLAYERS_PER_TEAM)]
        self.SPAWN_POSITIONS_TEAM_2 = [(self.SPAWN_OFFSET+i*self.SPAWN_OFFSET, self.WINDOW_HEIGHT-self.BLOCKSIZE) for i in range(self.NUM_PLAYERS_PER_TEAM)]

        self.TEAM1 = [Player(tag=f"p{i}_t1", spawnPosition=self.SPAWN_POSITIONS_TEAM_1[i]) for i in range(self.NUM_PLAYERS_PER_TEAM)]
        self.TEAM1_REMAINING = len(self.TEAM1)
        self.TEAM2 = [Player(tag=f"p{i}_t2", spawnPosition=self.SPAWN_POSITIONS_TEAM_2[i]) for i in range(self.NUM_PLAYERS_PER_TEAM)]
        self.TEAM2_REMAINING = len(self.TEAM2)

        if OBSTACLES:
            self.NUM_OBSTACLES = NUM_OBSTACLES
            self.OBSTACLES_POSITIONS = [(260, 260), (200, 180), (140, 240), (100, 160), (160, 340)]
        else:
            self.NUM_OBSTACLES = 0
            self.OBSTACLES_POSITIONS = [(0,0) for _ in range(self.NUM_OBSTACLES)]

    def designInterface(self):
        for x in range(0, self.WINDOW_WIDTH, self.BLOCKSIZE):
            for y in range(0, self.WINDOW_HEIGHT, self.BLOCKSIZE):
                pg.draw.rect(self.SCREEN, (200, 200, 200), pg.Rect(x, y, self.BLOCKSIZE, self.BLOCKSIZE), 1)

    def spawnPlayers(self):
        for coordinates in self.SPAWN_POSITIONS_TEAM_1:
            pg.draw.rect(self.SCREEN, (200, 200, 200), pg.Rect(coordinates[0], coordinates[1], self.BLOCKSIZE, self.BLOCKSIZE), 0)
        for coordinates in self.SPAWN_POSITIONS_TEAM_2:
            pg.draw.rect(self.SCREEN, (200, 200, 200), pg.Rect(coordinates[0], coordinates[1], self.BLOCKSIZE, self.BLOCKSIZE), 0)

    def spawnMovedPlayers(self):
        for player in self.TEAM1:
            if player.isAlive:
                pg.draw.rect(self.SCREEN,
                            (200, 200, 200),
                            pg.Rect(player.position[0], player.position[1], self.BLOCKSIZE, self.BLOCKSIZE),
                            0)
        for player in self.TEAM2:
            if player.isAlive:
                pg.draw.rect(self.SCREEN,
                            (200, 200, 200),
                            pg.Rect(player.position[0],
                            player.position[1], self.BLOCKSIZE, self.BLOCKSIZE),
                            0)

    def get_new_player_position_team1(self, position):
        # always returns a new position for team1 players within map's borders.
        search = True
        while search:
            random_direction = np.random.randint(low=1, high=5)#high excluded!
            #print(random_direction)
            # 1 -> Nord
            # 2 -> Est
            # 3 -> Sud
            # 4 -> Ovest
            if random_direction == 1 and position[1]+self.BLOCKSIZE<self.NORMALIZED_WINDOW_HEIGHT and position[1]+self.BLOCKSIZE >= 0:
                search = False
                return (position[0], position[1]+self.BLOCKSIZE)

            if random_direction == 2 and position[0]+self.BLOCKSIZE<self.NORMALIZED_WINDOW_WIDTH and position[0]+self.BLOCKSIZE>=0:
                search = False
                return (position[0]+self.BLOCKSIZE, position[1])
            
            if random_direction == 3 and position[1]-self.BLOCKSIZE<self.NORMALIZED_WINDOW_HEIGHT and position[1]-self.BLOCKSIZE>=0:
                search = False
                return (position[0], position[1]-self.BLOCKSIZE)
            
            if random_direction == 4 and position[0]-self.BLOCKSIZE<self.NORMALIZED_WINDOW_WIDTH and position[0]-self.BLOCKSIZE>=0:
                search = False
                return (position[0]-self.BLOCKSIZE, position[1])

    def get_new_player_position_team2(self, position):
        # always returns a new position for team2 players within map's borders.
        # for team2 players the situation is different:
        # they already spawn at (0-20-40-60-80, 400), so for them
        # north is south! 
        search = True
        while search:
            random_direction = np.random.randint(low=1, high=5)
            # 1 -> Nord (Sud)
            # 2 -> Est
            # 3 -> Sud (Nord)
            # 4 -> Ovest
            if random_direction == 1 and position[1]-self.BLOCKSIZE<self.NORMALIZED_WINDOW_HEIGHT and position[1]-self.BLOCKSIZE >= 0:
                search = False
                return (position[0], position[1]-self.BLOCKSIZE)

            if random_direction == 2 and position[0]+self.BLOCKSIZE<self.NORMALIZED_WINDOW_WIDTH and position[0]+self.BLOCKSIZE >= 0:
                search = False
                return (position[0]+self.BLOCKSIZE, position[1])
            
            if random_direction == 3 and position[1]+self.BLOCKSIZE<self.NORMALIZED_WINDOW_HEIGHT and position[1]+self.BLOCKSIZE >= 0:
                search = False
                return (position[0], position[1]+self.BLOCKSIZE)
            
            if random_direction == 4 and position[0]-self.BLOCKSIZE<self.NORMALIZED_WINDOW_WIDTH and position[0]-self.BLOCKSIZE >= 0:
                search = False
                return (position[0]-self.BLOCKSIZE, position[1])

    def spawnDeadPlayers(self):
        for player in self.TEAM1:
            if not player.isAlive:
                pg.draw.rect(self.SCREEN, (0, 255, 0), pg.Rect(player.position[0], player.position[1], self.BLOCKSIZE, self.BLOCKSIZE), 0)
        for player in self.TEAM2:
            if not player.isAlive:
                pg.draw.rect(self.SCREEN, (255, 0, 0), pg.Rect(player.position[0], player.position[1], self.BLOCKSIZE, self.BLOCKSIZE), 0)
                
    def spawnObstacles(self):
        for coordinates in self.OBSTACLES_POSITIONS:
            pg.draw.rect(self.SCREEN, (255, 0, 255), pg.Rect(coordinates[0], coordinates[1], self.BLOCKSIZE, self.BLOCKSIZE), 0)

    def interfaceSetup(self):
        self.designInterface()
        self.spawnPlayers()
        self.spawnObstacles()

    def clean_interface(self):
        self.SCREEN.fill((0, 0, 0))
        self.designInterface()

    def movePlayers(self):
        for player1 in self.TEAM1:
            looking_for_new_position = True
            if player1.isAlive:
                #continuo a cercare una nuova posizione finchè non ne trovo una adeguta
                while looking_for_new_position:
                    new_position = self.get_new_player_position_team1(player1.position)
                    if(new_position not in self.OBSTACLES_POSITIONS):
                        player1.move(new_position)
                        # print(f"Player {player1.tag} moved to {player1.position}")
                        looking_for_new_position = False


        for player2 in self.TEAM2:
            looking_for_new_position = True
            if player2.isAlive:
                #continuo a cercare una nuova posizione finchè non ne trovo una adeguta
                while looking_for_new_position:
                    new_position = self.get_new_player_position_team2(player2.position)
                    if(new_position not in self.OBSTACLES_POSITIONS):
                        player2.move(new_position)
                        # print(f"Player {player2.tag} moved to {player2.position}")
                        looking_for_new_position = False

    def resolveBattles(self):
        for player1 in self.TEAM1:
            for player2 in self.TEAM2:
                if player1.position == player2.position and player1.isAlive and player2.isAlive:
                    # scelgo un numero a caso tra 0 ed 1
                    # se questo è maggiore di .5 allora vince player del team1
                    # altrimenti vince player del team2                    
                        win_flag = np.random.random()

                        if win_flag > 0.5:
                            player1.addKill()
                            player2.die()
                            self.TEAM2_REMAINING -= 1
                            pg.draw.rect(self.SCREEN,
                                        (255, 0, 0),
                                        pg.Rect(player2.position[0], player2.position[1], self.BLOCKSIZE, self.BLOCKSIZE),
                                        0)
                        else:
                            player2.addKill()
                            player1.die()
                            self.TEAM1_REMAINING -= 1
                            pg.draw.rect(self.SCREEN,
                                        (0, 255, 0),
                                        pg.Rect(player1.position[0], player1.position[1], self.BLOCKSIZE, self.BLOCKSIZE),
                                        0)

                        self.NUM_PLAYERS_ALIVE -= 1

    def print_victory(self, team):
        print(f"{team} won!")
        pg.quit()
        sys.exit()

    def drawNewInterface(self):
        self.designInterface()
        self.spawnMovedPlayers()
        self.spawnDeadPlayers()
        self.spawnObstacles()

    def startGame(self):
        pg.init()

        self.SCREEN.fill((0, 0, 0))#filling the screen with black
        
        self.interfaceSetup()
        self.debug()
        
        while True:
            #EVENT LOOP
            self.movePlayers()
            self.resolveBattles()
            self.clean_interface()
            self.drawNewInterface()

            #check if a team won
            if self.TEAM1_REMAINING == 0:
                self.print_victory("TEAM 2")
            
            if self.TEAM2_REMAINING == 0:
                self.print_victory("TEAM 1")

            for e in pg.event.get():
                if e.type==pg.QUIT:
                    pg.quit()
                    sys.exit()
            # time.sleep(.1)
            pg.display.update()

    def debug(self):
        # pg.draw.rect(self.SCREEN, (0, 255, 0), pg.Rect(0, 0, self.BLOCKSIZE, self.BLOCKSIZE), 0)
        # pg.draw.rect(self.SCREEN, (255, 0, 0), pg.Rect(400, 0, self.BLOCKSIZE, self.BLOCKSIZE), 0)
        # pg.draw.rect(self.SCREEN, (0, 255, 255), pg.Rect(0, 400, self.BLOCKSIZE, self.BLOCKSIZE), 0)
        # pg.draw.rect(self.SCREEN, (255, 0, 255), pg.Rect(400, 400, self.BLOCKSIZE, self.BLOCKSIZE), 0)

        # print(self.WINDOW_HEIGHT)
        # print(self.WINDOW_WIDTH)

        # for player in self.TEAM1:
        #     print(player.spawnPosition)
        # for player in self.TEAM2:
        #     print(player.spawnPosition)
        pass