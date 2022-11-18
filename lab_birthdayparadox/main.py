import argparse

import numpy as np

from utils import *

from tabulate import tabulate

parser = argparse.ArgumentParser()
parser.add_argument("--prop-upper-bound", type=int, help="Upper bound for the generation of the desired property.", default=365)
parser.add_argument("--num-instances", type=int, help="Maximum objects' set's cardinality.", default=110)
args = parser.parse_args()

# setting a single seed since each run is independent from the other
SEED = 299266
np.random.seed(SEED)

EXP_PER_INSTANCE = 100
INSTANCES = [i for i  in range(10, 110, 10)]
DIST_TYPEs = ["uniform", "real"]  

def main():
    # for each kind of property distribution
    for dist_type in DIST_TYPEs:
        print(f"Using {dist_type} to generate property")
        # for each cardinality of the set under study
        global_lengths = list()
        global_probs = list()
        for cardinality in INSTANCES:
            print(f"\tWorking with cardinality: {cardinality}. Performing {EXP_PER_INSTANCE} experiments")
            # study the average number of objects to experience a conflict w.r.t. their property

            # study the probability of observing a conflict
            local_probs = list()
            counter = 0
            for _ in range(EXP_PER_INSTANCE):
                if dist_type=="uniform":
                    new_set = generate_uniform_set(m=cardinality, upper_bound=args.prop_upper_bound)
                else:
                    new_set = generate_real_set()
                if check_for_conflicts(test_set=new_set, upper_bound=args.prop_upper_bound):
                    counter += 1
            local_probs.append(counter/EXP_PER_INSTANCE)
            global_probs.append(np.mean(local_probs))
            global_lengths.append(len(new_set))

        plot_result(title=f"Conflicts happening with {dist_type} distribution for property",
                    filepath="results/",
                    filename=f"{dist_type}.png",
                    events=global_lengths,
                    probs=global_probs)
                

if __name__ == "__main__":
    main()