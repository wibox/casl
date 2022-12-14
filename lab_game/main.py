from interface import Interface
from logger import Logger

import argparse

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--area', type=int, default=200)
    parser.add_argument('--speed', type=int, default=1)
    parser.add_argument('--players', type=int, default=2)
    parser.add_argument('--seed', type=int, default=299266)

    return parser.parse_args()

args = parse_args()

myLogger = Logger(log_path="log")

if __name__ == "__main__":
    print(f"Testing: \n area = {args.area**2} \n speed = {args.speed} \n players = {args.players}")
    myGame = Interface(
        logger=myLogger,
        paths=myLogger.log_files,
        WINDOW_HEIGHT=args.area,
        WINDOW_WIDTH=args.area,
        NUM_PLAYERS_PER_TEAM=args.players,
        MOVEMENT_SPEED=args.speed,
        GAME_SPEED=.01
    )
    myGame.startGame()
