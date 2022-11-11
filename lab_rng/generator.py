import numpy as np
import scipy.special as ss
import matplotlib.pyplot as plt

from scipy.stats import binom

import time

def plot_pdf(x, pdf):
    """
    The only role of this function is to plot a specific pdf thorugh the corresponding boolean variable.
    """
    fig, ax = plt.subplots(figsize=(5,5))
    ax.plot(x, pdf, color="red")
    ax.set_xlabel("Points")
    ax.set_ylabel("Density")
    plt.suptitle("Normal PDF")
    plt.show()

def plot_rv(results, probs, num_istances):
    """
    The only role of this function is to plot a specific pdf thorugh the corresponding boolean variable.
    """
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

def log_exp_factorial(n):
    fact = 0
    for nn in range(n):
        fact += np.log(nn+1)
    
    return np.exp(fact)

def binomial_coeff(n, k):
    """
    This function computes the binomial coefficient using log (multiplications become sums) and then exp to get back
    the original result. The actual method that performs the logtrick is log_exp_factorial.
    """
    return log_exp_factorial(n)/((log_exp_factorial(k))*(log_exp_factorial(n-k)))

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
    probs_success = [binomial_coeff(n, success)*(p**success)*((1-p)**(n-success)) for success in range(n)]
    # log_probs_success = [ss.binom(n, success) + success*np.log(p) + (n-success)*np.log(1-p) for success in range(n)]
    # probs_success = [np.exp(prob) for prob in log_probs_success]
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

def binomial_inverse_no_of(n, p, num_istances, plot_pmf_probs):
    """
    This function uses scipy.stats.binom to generate the cdf instead of building it manually.
    """
    start_time = time.time()
    probs_success = [binom.cdf(success, n, p) for success in range(1,n)]

    u = np.random.uniform(low=0, high=1)

    results = []

    for take in range(num_istances):
        for x in range(n-1):
            if u >= probs_success[x] and u <= probs_success[x+1]:
                results.append(x)
    
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

def normal_dist(x, mean, s):
    return 1/np.sqrt(2*np.pi*s) * np.exp(-0.5*((x-mean)/s)**2)

def normal_acceptance(num_points, mean, s, a, b, num_istances, plot_pdf):
    """
    This function generates an istance of a normal random variable according to the acceptance/rejecton method.
    """
    start_time = time.time()
    space = np.linspace(a, b, num_points)
    dist = normal_dist(space, mean, s)

    results = []

    c = np.max(dist)
    for _ in range(num_istances):
        found = False
        if not found:
            x = np.random.uniform(low=a, high=b)
            y = np.random.uniform(low=0, high=c)
            if y <= normal_dist(x, mean, s):
                found = True
                results.append(y)

    if plot_pdf:
        plot_pdf(space, dist)

    if num_istances == 1:
        return results, dist, start_time-time.time()
    else:
        return results[0], dist, start_time-time.time()

def poisson(l):
    """
    This function generates an istance of a poisson distributed random variable with parameter l using Knuth algorithm.
    """
    n, q = 0, 1
    found = False
    while not found:
        u = np.random.uniform(low=0, high=1)
        q = q*u
        if q < np.exp(-l):
            found=True
            return n
        else:
            n += 1
    return 0

def chisquared(n):
    """
    This function generated an istance of a chisquared-distrubted random variable with parameter n using convolution method.
    """
    normals = [np.random.normal(loc=0, scale=1) for _ in range(n)]
    return sum(normals)

def rice(n, s):
    """
    This function generates a random variable distributed according to the Rice distribution X ~ R(n, s).
    Strategy:
        - Generate N ~ Poisson(k) with k = n^2 / 2s^2
        - Generate W ~ ChiSquared(2N+2)
        - Then R = s*sqrt(W) is rician-distributed.
    """
    #Generating poisson distributed r.v.
    l = n**2/(2*s**2)
    N = poisson(l)
    #Generating chisquared distributed r.v.
    W = chisquared(2*N+2)
    #Generating Rice.
    return s*np.sqrt(W)

def normal_confrontation(num_istances):
    
    istances = np.array([
        normal_acceptance(num_points=100, mean=0, s=1, a=-5, b=5, num_istances=1, plot_pdf=False) for _ in range(num_istances)
    ])
    return istances.mean, istances.std