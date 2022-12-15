from gwprocess import GWProcess

LAMBDAS = [0.6, 0.8, 0.9, 0.95, 0.99, 1.01, 1.05, 1.1, 1.3] # expected number of children per generation
NUMBER_OF_RUNS = 100 # number of runs for each gw process
GENERATIONS_THR = 70 # after 50 generation P[extinction] approx. 1

if __name__ == "__main__":

    for _lambda in LAMBDAS:
        # defining working regime
        if _lambda < 1:
            regime = "subcritical"
        elif _lambda > 1:
            regime = "supercritical"
        print(f"Using lambda: {_lambda} -> Regime: {regime}")
        # performing NUMBER_OF_RUNS for each _lambda
        for simulation_idx in range(NUMBER_OF_RUNS):

            gwp = GWProcess(
                _lambda=_lambda,
                max_generation=GENERATIONS_THR)