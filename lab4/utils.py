import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import t

def log_tot(bins, balls):
    for bin, ball in zip(bins, balls):
        print(f"{bin}\n{ball}")

def log(bins):
    result = [bin.num_balls for bin in bins]
    max_occ = max(result)
    min_occ = min(result)
    return max_occ, min_occ

def log_file_header(filename, header):
    with open(filename, "w") as f:
        f.write(header)

def log_to_file(filename, entry):
    with open(filename, "a") as f:
        f.write(entry)

def visualize_barplots(figname, max_rnd, max_ld2, max_ld4, num_experiments, save_bool):
    
    bar_width = .3
    bar_heigths = [max(max_rnd), max(max_ld2), max(max_ld4)]
    x_positions = np.arange(num_experiments)
    
    rnd_interval = t.interval(confidence=.99, df=num_experiments, loc=np.mean(max_rnd), scale=np.var(max_rnd))
    rnd_diff = rnd_interval[1] - rnd_interval[0]

    ld2_interval = t.interval(confidence=.99, df=num_experiments, loc=np.mean(max_ld2), scale=np.var(max_ld2))
    ld2_diff = ld2_interval[1] - ld2_interval[0]

    ld4_interval = t.interval(confidence=.99, df=num_experiments, loc=np.mean(max_ld4), scale=np.var(max_ld4))
    ld4_diff = ld4_interval[1] - ld4_interval[0]

    error_bars_height = [
            rnd_diff,
            ld2_diff,
            ld4_diff
        ]

    plt.bar(x_positions, bar_heigths, width = bar_width, color = 'blue', edgecolor = 'black', yerr=error_bars_height, capsize=7, label='Max occupancy for each policy')
    plt.xticks([r for r in range(num_experiments)], ['Random Dropping', 'Load Balancing 2', 'Load Balancing 4'])
    plt.ylabel('Max Occupancy')
    plt.legend()
    plt.grid()
    plt.show()
    if save_bool:
        plt.savefig(f"{figname}.svg")

def confidence_interval(vector):
    return t.interval(confidence=.9, df=3, loc=np.mean(vector), scale=np.var(vector))

def ci_vis(filenames, save_bool):
    fig, ax = plt.subplots(figsize=(15, 20), nrows=len(filenames))

    for filename, idx in zip(filenames, range(len(filenames))):
        df = pd.read_csv(filename)
        alg = filename.split(".")[0].split("_")[1]
        sns.lineplot(
            ax=ax[idx],
            x=df.iloc[:, 0],
            y=df.iloc[:, 1],
            data=df,
            errorbar="ci",
            linewidth=0.5
        )

        ax[idx].set_title(f"{alg} policy performance and confidence interval", fontweight = "bold")
        ax[idx].set_xscale("log")
        ax[idx].set_xlabel("Number of elements")
        ax[idx].set_ylabel("Maximum occupancy")
        ax[idx].grid()

    if save_bool:
        plt.savefig("results.svg")