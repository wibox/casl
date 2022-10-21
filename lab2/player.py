class Player():
    """
    class_attributes:
        -tag
        -spawn position: Tuple(int, int)
        -position: Tuple(int, int)
        -number of killed opponents: int
        -winner: bool
    class_methods:
        -move()
        -addKill()
        -die()
        -__str__()
    """
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
        pass

    def die(self):
        pass

    def __str__(self) -> str:
        return f"Return useful formatted string"