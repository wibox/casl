import argparse

import numpy as np

from utils import *

from tabulate import tabulate
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("--prop-upper-bound", type=int, help="Upper bound for the generation of the desired property.", default=365)
parser.add_argument("--num-instances", type=int, help="Maximum objects' set's cardinality.", default=110)
parser.add_argument("--real-data", type=str, help="Filename corresponding to the real distribution of birthdays.", default="US_births_2000-2014_SSA.csv")
args = parser.parse_args()

# setting a single seed since each run is independent from the other
SEED = 299266
np.random.seed(SEED)

EXP_PER_INSTANCE = 100
INSTANCES = [i for i  in range(10, 110, 10)]
DIST_TYPES = ["uniform", "real"]
UPPER_BOUNDS = [50, 500, 1000] 

def main():
    # for each kind of property distribution
    avg_dict = {"dist_type":["Average Cardinality", "C.I.", "Theory avg. cardinality"]}
    print(f"Working with property's upper bound: {args.prop_upper_bound}")
    for dist_type in DIST_TYPES:
        print(f"\nUsing {dist_type} distribution to generate property")
        # for each cardinality of the set under study
        global_lengths = list()
        global_probs = list()
        # study the average number of objects to experience a conflict w.r.t. their property
        avg_cardinality, glob_list = retrieve_avg_cardinality(
                                                    experiments=EXP_PER_INSTANCE,
                                                    dist_type=dist_type,
                                                    probs=generate_real_probs(args.real_data),
                                                    prop_upper_bound=args.prop_upper_bound
                                                    )
        # building the confidence interval for such measure
        avg_ci = generate_avg_ci(cardinalities=glob_list)
        # storing the final results for later logging
        avg_dict[f"{dist_type}"] = [avg_cardinality, avg_ci, 1.25*np.sqrt(args.prop_upper_bound)]

        # prob. study
        for cardinality in INSTANCES:
            print(f"\tWorking with cardinality: {cardinality}. Performing {EXP_PER_INSTANCE} experiments")
            # study the probability of observing a conflict
            local_probs = list()
            counter = 0
            for _ in tqdm(range(EXP_PER_INSTANCE)):

                if dist_type=="uniform":
                    new_set = generate_uniform_set(m=cardinality, prop_upper_bound=args.prop_upper_bound)
                else:
                    probs = generate_real_probs(filename=args.real_data)
                    new_set = generate_real_set(m=cardinality, prop_upper_bound=args.prop_upper_bound, probs=probs)

                if check_for_conflicts(test_set=new_set, prop_upper_bound=args.prop_upper_bound):
                    counter += 1

            local_probs.append(counter/EXP_PER_INSTANCE)
            global_probs.append(np.mean(local_probs))
            global_lengths.append(len(new_set))
            # computing confidence interval for global_probs
            upper_bound, lower_bound = generate_prob_ci(probs=global_probs, experiments=EXP_PER_INSTANCE)
            # building theoreical result
            theo_prob = theoretical_prob(m=global_lengths, prop_upper_bound=args.prop_upper_bound)

        # plot final results
        plot_results(title=f"Conflicts happening with {dist_type} distribution for property (birthday)",
                    filepath="results/",
                    filename=f"{dist_type}",
                    events=global_lengths,
                    exp_probs=global_probs,
                    upper_probs=upper_bound,
                    lower_probs=lower_bound,
                    theo_probs=theo_prob,
                    savefig_bool=True)
    # final logging
    print("\n\t FINAL RESULTS PER DISTRIBUTION:")
    print(tabulate(avg_dict, headers=["Uniform", "Real",], tablefmt="fancy_grid"))

    print(f"Simulating various property's upper bounds: {UPPER_BOUNDS}")
    dist_type = DIST_TYPES[0]
    exp_probs = list()
    theo_probs = list()
    upper_bounds = list()
    lower_bounds = list()
    for upper_bound in UPPER_BOUNDS:
        print(f"Working with property's upper bound: {upper_bound}")
        global_lengths = list()
        global_probs = list()
        for cardinality in INSTANCES:
            # study the probability of observing a conflict
            local_probs = list()
            counter = 0
            for _ in range(EXP_PER_INSTANCE):

                if dist_type=="uniform":
                    new_set = generate_uniform_set(m=cardinality, prop_upper_bound=args.prop_upper_bound)
                else:
                    probs = generate_real_probs(filename=args.real_data)
                    new_set = generate_real_set(m=cardinality, prop_upper_bound=args.prop_upper_bound, probs=probs)

                if check_for_conflicts(test_set=new_set, prop_upper_bound=args.prop_upper_bound):
                    counter += 1

            local_probs.append(counter/EXP_PER_INSTANCE)
            global_probs.append(np.mean(local_probs))
            global_lengths.append(len(new_set))
            # computing confidence interval for global_probs
            upper_bound, lower_bound = generate_prob_ci(probs=global_probs, experiments=EXP_PER_INSTANCE)
            # building theoreical result
            theo_prob = theoretical_prob(m=global_lengths, prop_upper_bound=args.prop_upper_bound)
        theo_probs.append(theo_prob)
        exp_probs.append(global_probs)
        upper_bounds.append(upper_bound)
        lower_bounds.append(lower_bound)

    plot_upper_bounds(title=f"Probability in function of property's upper bound ({dist_type} dist.)",
                    filepath="results/",
                    filename=f"upper_bounds_{dist_type}",
                    events=INSTANCES,
                    exp_probs=exp_probs,
                    upper_probs=upper_bounds,
                    lower_probs=lower_bounds,
                    theo_probs=theo_probs,
                    labels=[str(upper_bound) for upper_bound in UPPER_BOUNDS],
                    savefig_bool=True)
                
if __name__ == "__main__":
    main()