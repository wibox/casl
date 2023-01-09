import json
import traceback
import os

from typing import *

from scipy.stats import t
import numpy as np
import matplotlib.pyplot as plt

class Logger():
    """
    Simple Logger class employed in logging basic information about the ongoing Hawkes Process
    Args:
        verbosity: verbosity level for logging various types of messages. Suggested: 0
    """
    def __init__(
        self,
        verbosity : int = 1
    ):
        self.verbosity=verbosity

    def log_lp_msg(self, msg : str) -> None:
        if self.verbosity >= 1:
            print(msg)
    
    def log_hp_msg(self, msg : str) -> None:
        if self.verbosity >= 0:
            print(msg)
    
    def log_general_msg(self, msg : str) -> None:
        if self.verbosity == 0:
            print(msg)

class Constants:
    """
    Wrapper final class for the most used constants.
    """
    LOG_FOLDER_PATH = "log"
    PLOT_FOLDER_PATH = "plots"

    SEEDS = [299266, 247548, 777]#, 123456, 124056]
    h_t = ['uniform', 'exp']

    HAWKES_PROCESS_LOGFILENAME = "population.json"

class Helper:
    """
    Static class wrapping miscellaneous methods.
    """
    @staticmethod
    def plot_results(mean, lb, up, h):
        """
        Function used to plot requested informations.
        Args:
            ---
        Returns:
            None
        """
        fig, ax = plt.subplots(figsize=(6, 5))
        mean = sorted(mean)
        mean = np.array(mean)
        lb = np.array(sorted(lb))
        up = np.array(sorted(up))
        ax.plot([t for t in range(100)], mean)
        ax.fill_between([t for t in range(100)], mean, mean-lb, mean+up, alpha=.5)
        #ax.set_xticks([i for i in range(100)])
        plt.savefig(f"{h}_result.png")

    @staticmethod
    def format_output(width : int) -> None:
        """
        Routine employed in formatting logger's messages in the terminal.
        Args:
            width : int => should be os.get_terminal_size()[0]
        """
        for _ in range(width):
            print("=", end="")


    @staticmethod
    def log_json(filepath : str, filename : str, data : dict) -> bool:
        """
        Logs json serialized data to file.
        Args:
            filepath : str => desired log folder
            filename : str => desired log filename
            data : dict => python object to be json-serialized
        """
        completed = False
        try:
            with open(os.path.join(filepath, filename), "w") as fp:
                json.dump(data, fp, indent=4)
            completed = True
        except Exception as e:
            print(traceback.format_exc())
        finally:
            return completed

    @staticmethod
    def compute_populations_statistics(populations : List[Dict[int, int]]) -> None:
        mean_per_day : List[List[int]] = list()
        for key in range(100):
            day_infections_list : List[int] = list()
            for population in populations:
                day_infections_list.append(population[key])
            mean_per_day.append(day_infections_list)
        
        formatted_population : Dict[int, Tuple[float, float, float]] = dict()
        for key in range(100):
            bounds = t.interval(alpha=.05, df=4, loc=np.mean(mean_per_day[key]), scale=np.var(mean_per_day[key]))
            formatted_population[key] = (np.mean(mean_per_day[key]), bounds[0], bounds[1])

        return formatted_population
