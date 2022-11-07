import numpy as np

def random_dropping(balls, bins):
    for ball in balls:
        r = np.random.randint(low=0, high=len(bins))
        bins[r].drop_ball()
        ball.associate_bin(r)

def random_dropping_load_balancing(d, balls, bins):
    for ball in balls:
        random_bins = [(bins[np.random.randint(low=0, high=len(bins))]) for _ in range(d)]
        selected_bin = min(random_bins, key=lambda x : x.num_balls)
        selected_bin.drop_ball()
        ball.associate_bin(selected_bin.idx)