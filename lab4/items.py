class Bin():
    def __init__(self, idx):
        self.idx = idx
        self.num_balls = 0

    def drop_ball(self):
        self.num_balls += 1

    def __str__(self):
        return f"Bin {self.idx} has {self.num_balls} balls"

class Ball():
    def __init__(self, idx):
        self.idx = idx
        self.associated_bin = None

    def associate_bin(self, bin_idx):
        self.associated_bin = bin_idx

    def __str__(self):
        return f"Ball associated to bin {self.associated_bin}"