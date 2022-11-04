from items import Bin, Ball
from policy import *
from utils import *

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--num-items", type=int, default=1000)
parser.add_argument("--log-info", type=bool, default=False)
args = parser.parse_args()

SEEDS = [299266, 247548, 777, 9283570324]

def reset(num_items):
    global bins, balls
    bins = [Bin(idx) for idx in range(num_items)]
    balls = [Ball(idx) for idx in range(num_items)]

bins = list()
balls = list()

max_occ_rnd = list()
min_occ_rnd = list()

max_occ_ld2 = list()
min_occ_ld2 = list()

max_occ_ld4 = list()
min_occ_ld4 = list()

if __name__ == "__main__":
    for seed in SEEDS:
        print(f"Using seed: {seed}")

        # Random Dropping
        reset(args.num_items)
        random_dropping(bins=bins, balls=balls)
        max_occ, min_occ = log(bins)
        max_occ_rnd.append(max_occ)
        min_occ_rnd.append(min_occ)
        if args.log_info:
            print("LOGGING RANDOM DROPPING RESULTS")
            print(f"Maximum occupancy: {max_occ}\nMinum occupancy: {min_occ}\n#bins = #balls, average occupancy = 1")
        del bins, balls, max_occ, min_occ

        # Random dropping with load balancing (d=2)
        reset(args.num_items)
        random_dropping_load_balancing(d=2, bins=bins, balls=balls)
        max_occ, min_occ = log(bins)
        max_occ_ld2.append(max_occ)
        min_occ_ld2.append(min_occ)
        if args.log_info:
            print("LOGGING RANDOM DROPPING WITH LOAD BALANCING, D=2")
            print(f"Maximum occupancy: {max_occ}\nMinum occupancy: {min_occ}\n#bins = #balls, average occupancy = 1")
        del bins, balls, max_occ, min_occ

        # Random dropping with load balancing (d=4)
        reset(args.num_items)
        random_dropping_load_balancing(d=4, bins=bins, balls=balls)
        max_occ, min_occ = log(bins)
        max_occ_ld4.append(max_occ)
        min_occ_ld4.append(min_occ)
        if args.log_info:
            print("LOGGING RANDOM DROPPING WITH LOAD BALANCING, D=4")
            print(f"Maximum occupancy: {max_occ}\nMinum occupancy: {min_occ}\n#bins = #balls, average occupancy = 1")

    visualize_barplots("results", max_occ_rnd, max_occ_ld2, max_occ_ld4, num_experiments=len(SEEDS)-1)