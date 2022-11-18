import argparse

import numpy as np

from utils import *

parser = argparse.ArgumentParser()
parser.add_argument("--prop-upper-bound", type=int, default=365)
parser.add_argument("--num-instances", type=int, default=10)
args = parser.parse_args()

# setting a single seed since each run is independent from the other
SEED = 299266
np.random.seed(SEED)

INSTANCES = [i for i  in range(10, 110, 10)]

def main():

    conflicts = list()
    lengths = list()
    probs = list()
    counter = 0
    
    for instances in INSTANCES:
        new_set = generate_uniform_set(m=instances, upper_bound=args.prop_upper_bound)
        conflict, local_counter = check_for_conflicts(test_set=new_set, upper_bound=args.prop_upper_bound)
        counter += local_counter
        if conflict:
            conflicts.append(len(new_set))
        lengths.append(len(new_set))
        probs.append(counter/len(INSTANCES))
    print(f"Average: {np.mean(conflicts)}")
    plot_result(title="uniform", filepath="results/", filename="uniform_test.svg", events=lengths, probs=probs)


if __name__ == "__main__":
    main()