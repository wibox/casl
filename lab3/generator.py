import numpy as np
import scipy.special as ss
import matplotlib.pyplot as plt
import time

def plot_rv(results, probs, num_istances):
    fig, ax = plt.subplots(1, 2, figsize=(5,5))

    ax[0].scatter([i for i in range(num_istances)], probs)
    ax[1].scatter([i for i in range(num_istances)], results)

    ax[0].legend(["Probabilities"])
    ax[1].legend(["Istances"])

    ax[0].set_ylabel("Probabilities")
    ax[0].set_xlabel("Realizations")

    ax[1].set_ylabel("Istances")
    ax[1].set_xlabel("Realizations")
    plt.suptitle("Binomial generation through convolution")
    plt.show()

def binomial_convolution(n, p, num_istances, plot_pmf_probs):
    """
    Count the number of times a bernoulli(here a simple uniform) returns
    success, then return x
    """
    start_time = time.time()
    results = []
    probs = []
    
    #Generation of num_istances istances of the RV
    for take in range(num_istances):
        uniforms = np.random.uniform(low=0, high=1, size=10)
        x = np.count_nonzero(uniforms<p)
        results.append(x)

    #now we compute the probabilities associated to each istance of the RV
    for result in results:
        probs.append(ss.binom(n, result)*(p**result)*((1-p)**(n-result)))

    if plot_pmf_probs:
        plot_rv(results, probs, num_istances)

    return results, probs, time.time()-start_time

def binomial_inverse(n, p, num_istances, plot_pmf_probs):
    """
    Define CDF(x). Generate U ~ Uniform(0, 1) and lookup X in CDF(x) array. Return x
    """
    start_time = time.time()
    #probabilities of k positive outcomes
    # probs_success = [ss.binom(n, success)*(p**success)*((1-p)**(n-success)) for success in range(n)]
    log_probs_success = [ss.binom(n, success) + success*np.log(p) + (n-success)*np.log(1-p) for success in range(n)]
    probs_success = [np.exp(prob) for prob in log_probs_success]
    #number of positive outcomes
    positive_outcomes = [i for i in range(n)]
    results = []
    #to lookup the table just point the fact that pmf(x) is symmetric (so only the first tail has to be checked)
    for take in range(num_istances):
        found = False
        while not found:
            idx = 1
            u = np.random.uniform(low=0, high=1)
            for _ in range(len(probs_success)):
                if u > sum(probs_success[0:idx]) and u <= sum(probs_success[0:idx+1]):
                    found = True
                    results.append(positive_outcomes[idx-1])
                idx = idx + 1

    if plot_pmf_probs:
        plot_rv(results, probs_success, num_istances)

    return results, probs_success, time.time()-start_time

def binomial_empirical(n, p, num_istances, plot_pmf_probs):
    """
    Exploit geometric distribution with parameter 1-p, alg on slide 60
    """
    start_time = time.time()
    results = []
    probs = []

    for take in range(num_istances):
        m, q = 1, 0
        found = False
        while not found:
            u = np.random.uniform(low=0, high=1)
            g = np.ceil(np.log(u)/np.log(1-p))
            q = q + g
            if q > n:
                found = True
                results.append(m-1)
        
    for result in results:
        probs.append(ss.binom(n, result)*(p**result)*((1-p)**(n-result)))

    if plot_pmf_probs:
        plot_rv(results, probs, num_istances)

    return results, probs, time.time()-start_time

def normal_acceptance():
    pass

def rice():
    pass