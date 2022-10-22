from interface import Interface
from logger import Logger
from warhol import Warhol

myLogger = Logger()
myWarhol = Warhol()
myGame = Interface()

if __name__ == "__main__":
    myGame.startGame()