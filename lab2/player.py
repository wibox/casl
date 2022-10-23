class Player():
    def __init__(self, tag, spawnPosition, aos_metric):

        self.tag=tag
        self.spawnPosition=spawnPosition
        self.position=spawnPosition
        self.numKills=0
        self.isAlive=True
        self.isWinner=False
        self.aos_metric=aos_metric

        self.aos = [
                    (self.position[0]+self.aos_metric, self.position[1]),
                    (self.position[0], self.position[1]+self.aos_metric),
                    (self.position[0]-self.aos_metric, self.position[1]),
                    (self.position[0], self.position[1]-self.aos_metric),
                    (self.position[0]+self.aos_metric, self.position[1]+self.aos_metric),
                    (self.position[0]-self.aos_metric, self.position[1]-self.aos_metric),
                    (self.position[0]+self.aos_metric, self.position[1]-self.aos_metric),
                    (self.position[0]-self.aos_metric, self.position[1]+self.aos_metric)]

    def update_aos(self):
        self.aos = [
                    (self.position[0]+self.aos_metric, self.position[1]),
                    (self.position[0], self.position[1]+self.aos_metric),
                    (self.position[0]-self.aos_metric, self.position[1]),
                    (self.position[0], self.position[1]-self.aos_metric),
                    (self.position[0]+self.aos_metric, self.position[1]+self.aos_metric),
                    (self.position[0]-self.aos_metric, self.position[1]-self.aos_metric),
                    (self.position[0]+self.aos_metric, self.position[1]-self.aos_metric),
                    (self.position[0]-self.aos_metric, self.position[1]+self.aos_metric)]
    def move(self, position):
        self.position=position
        self.update_aos()

    def addKill(self):
        self.numKills += 1

    def die(self):
        self.isAlive=False

    def __str__(self) -> str:
        return f"Return useful formatted string"