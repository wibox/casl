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
    
    uniform_analysis(cardinalities=INSTANCES, upper_bound=args.prop_upper_bound)
    # real_analysis()

if __name__ == "__main__":
    main()