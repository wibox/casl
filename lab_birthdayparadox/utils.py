import numpy as np
import matplotlib.pyplot as plt

from typing import *
import os

class Property():
    def __init__(self, upper_bound):
        self.upper_bound = upper_bound
        self.prop = 0

    def generate_uniform_prop(self) -> int:
        self.prop = np.random.randint(low=1,high=self.upper_bound)
        return self.prop

class Obj():
    def __init__(self, id, prop):
        self.id = id
        self.prop = prop

    def __str__(self) -> str:
        return f"Object: {self.id} -> {self.prop}"

def generate_uniform_set(m : int, upper_bound : int) -> List[Obj]:
    """
    This function returns a list of object with a given property. According to the problem's specification
    this is just the id of the day of the year corresponding to the person's birthday.
    """
    return [Obj(id=i,prop=Property(upper_bound=365).generate_uniform_prop()).prop for i in range(m)]

def check_for_conflicts(test_set : List[Obj], upper_bound : int) -> Tuple[bool, int]:
    counter = 0
    lookup_table = [0 for _ in range(1, upper_bound + 1)]
    for prop in test_set:
        lookup_table[prop] += 1
        if lookup_table[prop] > 1:
            counter += 1
            return True, counter
    return False, counter

def plot_result(title : str, filepath : str, filename : str, events : List[int], probs : List[int], savefig_bool : bool = True) -> None:
    fig, ax = plt.subplots(figsize=(10, 15))
    ax.plot(events, probs)
    ax.set_xlabel("Size of instance")
    ax.set_ylabel("Probability to experience a conflict")
    plt.suptitle(title)
    plt.grid()
    plt.show()
    plt.savefig(os.path.join(filepath, filename))