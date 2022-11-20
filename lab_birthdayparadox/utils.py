import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as st

from typing import *
import os

class Property():
    """
    This class stores informations regarding a general property. In this specific case we are dealing with
    birthdays, but this structure is useful for further generalization.
    """
    def __init__(self, upper_bound):
        self.upper_bound = upper_bound
        self.uniform_prop = 0
        self.real_prop = 0

    def generate_uniform_prop(self) -> int:
        self.uniform_prop = np.random.randint(low=1,high=self.upper_bound)
        return self.uniform_prop

    def generate_real_prop(self, probs : List[float]) -> int:
        self.real_prop = np.random.choice(a=np.array(range(self.upper_bound)), p=probs)
        return self.real_prop

class Obj():
    """
    This class builds objects with a specific value for their property. Since we are dealing with birthdays
    each instance can be seen as a person with just one relevant property.
    """
    def __init__(self, id, uniform_prop=None, real_prop=None):
        self.id = id
        self.uniform_prop = uniform_prop
        self.real_prop = real_prop

    def __str__(self) -> str:
        return f"Object: {self.id} -> U:{self.uniform_prop} -> R:{self.real_prop}"

def retrieve_avg_cardinality(experiments : int, dist_type : str, probs : List[float], prop_upper_bound : int) -> Tuple[float, List[int]]:
    """
    Function used to retrieve the average cardinality of the set to experience a conflict. 
    It performs 100 experiments to establish such average.
    """
    glob_list = list()
    for _ in range(experiments):
        m = 0
        test_list = list()
        while True:
            if dist_type == "uniform":
                new_item = generate_uniform_instance(prop_upper_bound=prop_upper_bound, id=m)
            else:
                new_item = generate_real_instance(prop_upper_bound=prop_upper_bound, id=m, probs=probs)
            test_list.append(new_item)
            if check_for_conflicts(test_set=test_list, prop_upper_bound=prop_upper_bound):
                glob_list.append(m)
                break
            m += 1
    return np.sum(glob_list)/len(glob_list), glob_list


def generate_uniform_set(m : int, prop_upper_bound : int) -> List[Obj]:
    """
    This function returns a list of object with a given property. According to the problem's specification
    this is just the id of the day of the year corresponding to the person's birthday. The underlying distribution
    is Uniform.
    """
    return [Obj(id=i,uniform_prop=Property(upper_bound=prop_upper_bound).generate_uniform_prop()).uniform_prop for i in range(m)]

def generate_uniform_instance(prop_upper_bound : int, id : int) -> Obj:
    """
    Identical to generate_uniform_set() but returns just one instances.
    """
    return Obj(id=id,uniform_prop=Property(upper_bound=prop_upper_bound).generate_uniform_prop()).uniform_prop

def generate_real_set(m : int, prop_upper_bound : int, probs : List[float]) -> List[Obj]:
    """
    This function returns a list of objects with a given property. According to the probem's specification
    this is just the id of the day of the year corresponding to the person's birthday. The underlying distribution
    is retrieved from real data.
    """
    return [Obj(id=i,real_prop=Property(upper_bound=prop_upper_bound).generate_real_prop(probs=probs)).real_prop for i in range(m)]

def generate_real_probs(filename: str) -> List[float]:
    """
    This function returns the probabilities for each birthday according to a specific collection.
    The file used is in the current directory or can be found 
    @ https://github.com/fivethirtyeight/data/tree/master/births

    """
    b = pd.read_csv(filename).groupby(['month','date_of_month'])
    # removing leap year hor homogeneity w.r.t. the rest of the code
    total_day_per_month = b['births'].sum().drop((2, 29))
    total = total_day_per_month.sum() 
    probs = (total_day_per_month/total).values
    return probs

def generate_real_instance(prop_upper_bound : int, id : int, probs : List[float]) -> Obj:
    """
    Same function as generate_real_set() but returns just one instance.
    """
    return Obj(id=id,real_prop=Property(upper_bound=prop_upper_bound).generate_real_prop(probs=probs)).real_prop

def check_for_conflicts(test_set : List[Obj], prop_upper_bound : int) -> bool:
    """
    This functions checks if two objects experience a conflict w.r.t. their property in a specific list given as input.
    """
    lookup_table = [0 for _ in range(1, prop_upper_bound + 1)]
    for prop in test_set:
        lookup_table[prop] += 1
        if lookup_table[prop] > 1:
            return True
    return False

def generate_prob_ci(probs : List[float], experiments : int) -> Tuple[List[float], List[float]]:
    """
    According to theory, this function generates the confidence interval for the probability of experiencing a conflict.
    """
    upper_bound = list()
    lower_bound = list()

    cl = st.norm(loc=0, scale=1).ppf(.95)
    for prob in probs:
        s_hat = np.sqrt((prob*(1-prob))/experiments)
        interval = cl*s_hat
        upper_bound.append(prob+interval)
        lower_bound.append(prob-interval)
    
    return upper_bound, lower_bound

def generate_avg_ci(cardinalities : List[int]) -> float:
    """
    This function returns the confidence interval for the average cardinality experiencing a conflict.
    """
    ci = st.t.interval(alpha=0.05, df=len(cardinalities)-1, loc=np.mean(cardinalities), scale=np.var(cardinalities))
    return ci

def theoretical_prob(m : List[int], prop_upper_bound : int) -> List[float]:
    """
    Returns the theoretical probabilities according to the theory seen during lecture.
    """
    theo_prob = list()
    for cardinality in m:
        theo_prob.append(round(1 - pow(np.e, -1*(pow(cardinality,2))/(2*prop_upper_bound)), 5))
    return theo_prob

def plot_results(title : str,
                filepath : str,
                filename : str,
                events : List[int],
                exp_probs : List[float],
                theo_probs : List[float],
                upper_probs : List[float] = None,
                lower_probs : List[float] = None,
                savefig_bool : bool = True) -> None:

    fig, ax = plt.subplots(figsize=(10, 15))
    ax.plot(events, exp_probs, label="empirical probability")
    ax.plot(events, theo_probs, label="theoretical probability")
    if upper_probs and lower_probs:
        ax.fill_between(events, lower_probs, upper_probs, alpha=.5)
    ax.set_xlabel("Cardinality of set")
    ax.set_ylabel("Probability to experience a conflict")
    plt.title(title)
    plt.grid()
    plt.legend()
    plt.show()
    if savefig_bool:
        fig.savefig(os.path.join(filepath, filename))

    
def plot_upper_bounds(title : str,
                filepath : str,
                filename : str,
                events : List[int],
                exp_probs : List[List[float]],
                theo_probs : List[List[float]],
                labels : List[str],
                upper_probs : List[List[float]] = None,
                lower_probs : List[List[float]] = None,
                savefig_bool : bool = True) -> None:

    fig, ax = plt.subplots(figsize=(10, 15))
    for exp_prob, theo_prob, upper_prob, lower_prob, label in zip(exp_probs, theo_probs, upper_probs, lower_probs, labels):
        ax.plot(events, exp_prob, label=f"empirical probability - {label}")
        ax.plot(events, theo_prob, label=f"theoretical probability - {label}")
        if upper_prob and lower_prob:
            ax.fill_between(events, lower_prob, upper_prob, alpha=.5)
    ax.set_xlabel("Cardinality of set")
    ax.set_ylabel("Probability to experience a conflict")
    plt.title(title)
    plt.grid()
    plt.legend()
    plt.show()
    if savefig_bool:
        fig.savefig(os.path.join(filepath, filename))