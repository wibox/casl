from items import Bin, Ball
from policy import *
from utils import *

NUM_ITEMS = 20
# bins = [Bin(idx) for idx in range(NUM_BINS)]
# balls = [Ball(idx) for idx in range(NUM_BALLS)]

def reset(num_items):
    global bins, balls
    bins = [Bin(idx) for idx in range(num_items)]
    balls = [Ball(idx) for idx in range(num_items)]

bins = list()
balls = list()

if __name__ == "__main__":
    reset(NUM_ITEMS)
    random_dropping(bins=bins, balls=balls)
    print("LOGGING RANDOM DROPPING RESULTS")
    log(bins)
    del bins, balls
    reset(NUM_ITEMS)
    random_dropping_load_balancing(d=2, bins=bins, balls=balls)
    print("LOGGING RANDOM DROPPING WITH LOAD BALANCING, D=2")
    log(bins)
    del bins, balls
    reset(NUM_ITEMS)
    random_dropping_load_balancing(d=4, bins=bins, balls=balls)
    print("LOGGING RANDOM DROPPING WITH LOAD BALANCING, D=4")
    log(bins)