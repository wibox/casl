import numpy as np
np.random.seed(299266)
from collections import OrderedDict
import matplotlib.pyplot as plt
from typing import *
import os

LAMBDAS = [0.6, 0.8, 0.9, 0.95, 0.99, 1.01, 1.05, 1.1, 1.3] # expected number of children per generation
NUMBER_OF_RUNS = 100 # number of runs for each gw process
GENERATIONS_THR = 70 # after 50 generation P[extinction] approx. 1
GEN_DICT = OrderedDict()

def plot_results(x:List[int], y:List[float], y_theo:List[float], title:str, xlabel:str, ylabel:str, filename:str, filepath:str, save_fig_bool:bool) -> None:
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.plot(x, y, label="experimental")
    ax.plot(x, y_theo, label="theoretical")
    # here add confidence interval
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid()
    ax.legend()
    if save_fig_bool:
        plt.savefig(os.path.join(filepath, filename))
    plt.close()

def generate_generation_children(_lambda : int = 0):
    return np.random.poisson(lam=_lambda)

def run_simulation(_lambda : int = 0) -> Tuple[List[int], bool, bool, int]:
    extinction = False
    reached_max_gen = False
    running = True
    generation_counter = 0
    tree = np.zeros(GENERATIONS_THR) # list of children per generation
    tree[0] = 1
    while running:
        gen_children = generate_generation_children(_lambda=_lambda)
        if gen_children == 0:
            extinction = True
            running = False
            if generation_counter in GEN_DICT:
                GEN_DICT[generation_counter] += 1
            else:
                GEN_DICT[generation_counter] = 1
        if generation_counter==GENERATIONS_THR:
            reached_max_gen = True
            running = False
        generation_counter += 1
        tree[generation_counter] += gen_children
    return tree, extinction, reached_max_gen, generation_counter

if __name__ == "__main__":

    for _lambda in LAMBDAS:
        # defining working regime
        if _lambda < 1:
            regime = "subcritical"
        elif _lambda > 1:
            regime = "supercritical"
        print(f"Using lambda: {_lambda} -> Regime: {regime}")
        # performing NUMBER_OF_RUNS for each _lambda
        tree_08 = np.zeros(GENERATIONS_THR)
        for simulation_idx in range(NUMBER_OF_RUNS):
            tree, extinction, reached_max_gen, generation_counter = run_simulation(_lambda=_lambda)
            tree_08 = tree_08 + tree
        tree_08 = tree_08 / NUMBER_OF_RUNS
        GEN_DICT = OrderedDict(sorted(GEN_DICT.items(), key=lambda x: x[0]))
        probs = list()
        gens = list()
        for k in GEN_DICT.keys():
            GEN_DICT[k] = GEN_DICT[k]/NUMBER_OF_RUNS
            gens.append(k)
        for v in GEN_DICT.values():
            probs.append(v)

        if _lambda == 0.8:
            # here we get the histogram for this specific value of lambda
            fig, ax = plt.subplots(figsize=(5, 5))
            ax.bar(range(len(np.trim_zeros(tree_08))), np.trim_zeros(tree_08))
            ax.set_title("Exp. distribution of nodes per generation (lambda = 0.8)")
            ax.set_ylabel("Number of nodes")
            ax.set_xlabel("Generation")
            ax.grid()
            plt.savefig("results/histogram.png")
            plt.close()

        probs = np.cumsum(probs) # prob of extinction increases every generation according to prev. gen.
        for idx, prob in enumerate(probs):
            if prob > 1:
                probs[idx] = 1
        q = []
        q.append(np.exp(-_lambda))
        for i in range(1, len(probs)):
            q.append(np.exp(_lambda*(q[-1]-1)))

        plot_results(
            x = gens,
            y = probs,
            y_theo = q,
            title = f"Probability of extinction per generation (lambda:{_lambda})",
            xlabel = "Generation",
            ylabel = "Probability of extinction",
            filename = f"pvg_{_lambda}.png",
            filepath = "results",
            save_fig_bool = True
        )