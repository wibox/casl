import generator as g
import pandas as pd

NS = [10, 100, int(1e6)]
PROBABILITIES = [0.5, 0.01, 0.00001]
NUM_ISTANCES = 50

HEADER="method,n,p,time\n"

if __name__ == "__main__":

    with open("log.csv", "w") as f:
        f.write(HEADER)
    with open("log.csv", "a") as flog:
        for n, p in zip(NS, PROBABILITIES):
            results_conv, probs_conv, time_conv = g.binomial_convolution(n=n, p=p, num_istances=NUM_ISTANCES, plot_pmf_probs=False)
            flog.write(f"'conv',{n},{p},{time_conv}\n")
            results_inv, probs_inv, time_inv = g.binomial_inverse(n=n, p=p, num_istances=NUM_ISTANCES, plot_pmf_probs=False)
            flog.write(f"'inv',{n},{p},{time_inv}\n")
            results_exp, probs_exp, time_exp = g.binomial_empirical(n=n, p=p, num_istances=NUM_ISTANCES, plot_pmf_probs=False)
            flog.write(f"'exp',{n},{p},{time_exp}\n")

