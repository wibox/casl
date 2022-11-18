import argparse

import numpy as np

from utils import *

parser = argparse.ArgumentParser()
parser.add_argument("--prop-upper-bound", type=int, default=365)
parser.add_argument("--num-instances", type=int, default=10)
args = parser.parse_args()

# setting a singe seed since each run is independent from the other
SEED = 299266
np.random.seed(SEED)

# picking a random integer to decide the size of the set generator
# INSTANCES = [i for i in range(2, np.random.randint(low=10, high=100))]
INSTANCES = [i for i  in range(10, 110, 10)]

# list into which append the size of the set 
conflicts = list()
counter = 0
lengths = list()
probs = list()

if __name__ == "__main__":
    # first we evaluate the average number of people to experience a conflict with uniform dist.
    print(f"Finding average number of objects to experience a conflict when property is uniformely distributed...")
    for num_instances in INSTANCES:
        # generate a fixed sized set of instances with uniformely distributed property
        starting_set = generate_uniform_set(m=num_instances, upper_bound=args.prop_upper_bound)
        lengths.append(len(starting_set))
        print(f"\tWorking with set: \n\t\t{starting_set}")
        # check if a conflict is experienced
        conflict, instances = check_for_conflicts(test_set=starting_set, upper_bound=args.prop_upper_bound)
        if conflict:
            counter += 1
            print("\tConflict happened.")
            conflicts.append(instances)
        probs.append(counter/len(INSTANCES))
    print(f"Average number of objects to experience a conflict when property uniformely distributed: {np.mean(conflicts)}")
    # now we evaluate the probability of experiencing a conflict in function of m when property is uniformely distributed.
    plot_result(title="uniform", filepath="results/", filename="uniform_test.svg", events=lengths, probs=probs)