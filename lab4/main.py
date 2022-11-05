from items import Bin, Ball
from policy import *
from utils import *

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--log-info", type=bool, default=False)
args = parser.parse_args()

SEEDS = [299266, 247548, 777, 9283570324]
NUM_ELEMENTS = [10, 50, 100, 500, 750, 1000, 5000, 7500, 10000, 50000, 75000, 100000, 500000, 750000, 1000000]
LOGF = [
    "rnd",
    "ld2",
    "ld4"
]

def reset(num_items):
    global bins, balls
    bins = [Bin(idx) for idx in range(num_items)]
    balls = [Ball(idx) for idx in range(num_items)]

bins = list()
balls = list()

max_occ_rnd_arr = list()
min_occ_rnd_arr = list()

max_occ_ld2_arr = list()
min_occ_ld2_arr = list()

max_occ_ld4_arr = list()
min_occ_ld4_arr = list()

if __name__ == "__main__":
    # Writing headers to corresponding log files
    for fn in LOGF:
        log_file_header(filename=f"log_{fn}.csv", header="num_elements,max_occupancy,min_occupancy\n")

    for num_items in NUM_ELEMENTS:
        print(f"Using number of elements: {num_items}")
        for seed in SEEDS:
            print(f"\tUsing seed: {seed}")

            # Random Dropping
            reset(num_items)
            random_dropping(bins=bins, balls=balls)
            max_occ_rnd, min_occ_rnd = log(bins)
            max_occ_rnd_arr.append(max_occ_rnd)
            min_occ_rnd_arr.append(min_occ_rnd)
            if args.log_info:
                print("LOGGING RANDOM DROPPING RESULTS")
                print(f"Maximum occupancy: {max_occ_rnd}\nMinum occupancy: {min_occ_rnd}\n#bins = #balls, average occupancy = 1")
            del bins, balls

            # Random dropping with load balancing (d=2)
            reset(num_items)
            random_dropping_load_balancing(d=2, bins=bins, balls=balls)
            max_occ_ld2, min_occ_ld2 = log(bins)
            max_occ_ld2_arr.append(max_occ_ld2)
            min_occ_ld2_arr.append(min_occ_ld2)
            if args.log_info:
                print("LOGGING RANDOM DROPPING WITH LOAD BALANCING, D=2")
                print(f"Maximum occupancy: {max_occ_ld2}\nMinum occupancy: {min_occ_ld2}\n#bins = #balls, average occupancy = 1")
            del bins, balls

            # Random dropping with load balancing (d=4)
            reset(num_items)
            random_dropping_load_balancing(d=4, bins=bins, balls=balls)
            max_occ_ld4, min_occ_ld4 = log(bins)
            max_occ_ld4_arr.append(max_occ_ld4)
            min_occ_ld4_arr.append(min_occ_ld4)
            if args.log_info:
                print("LOGGING RANDOM DROPPING WITH LOAD BALANCING, D=4")
                print(f"Maximum occupancy: {max_occ_ld4}\nMinum occupancy: {min_occ_ld4}\n#bins = #balls, average occupancy = 1")

            # visualize_barplots("results", max_occ_rnd, max_occ_ld2, max_occ_ld4, num_experiments=len(SEEDS)-1, save_bool=False)
            # Logging informations to file
            log_to_file(filename="log_rnd.csv", entry=f"{num_items},{max_occ_rnd},{min_occ_rnd}\n")
            log_to_file(filename="log_ld2.csv", entry=f"{num_items},{max_occ_ld2},{min_occ_ld2}\n")
            log_to_file(filename="log_ld4.csv", entry=f"{num_items},{max_occ_ld4},{min_occ_ld4}\n")
    # Visualize final results
    ci_vis([f"log_{fn}.csv" for fn in LOGF], save_bool=True)