import generator as g
import pandas as pd

NS = [10, 100, int(1e6)]
PROBABILITIES = [0.5, 0.01, 1e-5]
NUM_ISTANCES = 50

HEADER="method,n,p,time\n"

if __name__ == "__main__":

    with open("log.csv", "w") as f:
        f.write(HEADER)

    with open("log.csv", "a") as f_log:
        for n, p in zip(NS, PROBABILITIES):
            print(f"Performing binomial with convolution. Parameters: \n n = {n} \n p = {p} \n")
            results_conv, probs_conv, time_conv = g.binomial_convolution(n=n, p=p, num_istances=NUM_ISTANCES, plot_pmf_probs=False)
            f_log.write(f"'conv',{n},{p},{time_conv}\n")
            print(f"Performing binomial with Inverse-Transform method. Parameters: \n n = {n} \n p = {p} \n")
            results_inv, probs_inv, time_inv = g.binomial_inverse_no_of(n=n, p=p, num_istances=NUM_ISTANCES, plot_pmf_probs=False)
            f_log.write(f"'inv',{n},{p},{time_inv}\n")
            print(f"Performing binomial with Emp. method. Parameters: \n n = {n} \n p = {p} \n")
            results_exp, probs_exp, time_exp = g.binomial_empirical(n=n, p=p, num_istances=NUM_ISTANCES, plot_pmf_probs=False)
            f_log.write(f"'exp',{n},{p},{time_exp}\n")
        
    print(f"Random Normal R.V. with acceptance/rejection method: {g.normal_acceptance(num_points=100, mean=0, s=1, a=-1, b=1, num_istances=1, plot_pdf=False)[0][0]}")
    print(f"Random Rician-distributed R.V. exploiting relation with Poisson and ChiSquared distribution: {g.rice(5, 3)}")

# Confrontation between real and acceptance/rejection normal dist with 200 istances of a standard normal r.v.
mean, std = g.normal_confrontation(200)
print(f"Theoretical values\n\t mean : 0 \n\t std : 0 \n Empirical values \n\t mean : {mean} \n\t std : {std}")
