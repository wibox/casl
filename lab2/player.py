class Player():
    def __init__(self, tag, spawnPosition):

        self.tag=tag
        self.spawnPosition=spawnPosition
        self.position=spawnPosition
        self.numKills=0
        self.isAlive=True
        self.isWinner=False

    def move(self, position):
        self.position=position

    def addKill(self):
        self.numKills += 1

    def die(self):
        self.isAlive=False

    def __str__(self) -> str:
        return f"Return useful formatted string"