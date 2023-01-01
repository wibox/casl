from .tokenizer import Tokenizer
from .fingerprint_handler import FingerprintHandler

from pympler import asizeof as ao
import matplotlib.pyplot as plt

import traceback
import json
import os

from typing import *

class Constants:

    LOG_FOLDER_PATH = "log/"
    PLOT_FOLDER_PATH = "plots/"
    
    FORMATTED_TEXT_FILENAME = "formatted_verses.txt"
    
    GRAM_FILENAME = "grams.txt"
    GRAM_SIZE = 6

    FP_FILENAME = "fp.txt"

    PRFPS_FILENAME = "prfps.txt"

    BSA_FILENAME = "bsa"

class Helper:

    @staticmethod
    def plot_results(
        x : List[List[float]],
        y : List[List[List[float]]],
        legend_handles : List[List[str]],
        xlabel : List[str],
        ylabel : List[str],
        ax_title : List[str],
        fig_title : str,
        save_fig_bool : bool,
        filepath : str,
        filename : str
    ) -> None:
        assert len(x) == len(y), "Size mismatch in input."
        num_plots = len(y)
        fig, axs = plt.subplots(1, num_plots, figsize=(6*num_plots, 5))
        fig.suptitle(fig_title)
        for x_el, y_el, legend_handle, xlabel_el, ylabel_el, title_el, idx in zip(x, y, legend_handles, xlabel, ylabel, ax_title, range(num_plots)):
            axs[idx].grid()
            for sub_y, sub_handle in zip(y_el, legend_handle):
                axs[idx].plot(x_el, sub_y, label=sub_handle)
                axs[idx].set_xlabel(xlabel_el)
                axs[idx].set_ylabel(ylabel_el)
                axs[idx].set_title(title_el)
                axs[idx].legend()

        if save_fig_bool:
            print(f"Saving picture in {os.path.join(filepath, filename)}")
            plt.savefig(os.path.join(filepath, filename))

    @staticmethod
    def log_json(filename : str, filepath : str, json_obj : Dict[int, float] = None) -> bool:
        completed = False
        try:
            with open(os.path.join(filepath, filename), "w") as outds:
                json.dump(json_obj, outds, indent=4)
            completed = True
        except Exception as e:
            print(traceback.format_exc())
        finally:
            return completed

    @staticmethod
    def compute_text_info(filename : str = "divina_commedia.txt", tokenizer : Tokenizer = Tokenizer()) -> Tuple[int, int, int, bool, List[str]]:
        completed = False
        try:
            with open(f"{filename}", "r") as divina_commedia:
                unique_words = set()
                formatted_lines = list()
                word_counter = 0
                verse_counter = 0            
                lines = divina_commedia.readlines()
                for line in lines:
                    #clean each line
                    line = tokenizer.clean_line(line)
                    formatted_lines.append(line)
                    #count #verses
                    if line != "":
                        verse_counter += 1
                    #count #words
                    word_counter += len(line.split(" "))
                    #count #unique words
                    for word in line.split(" "):
                        unique_words.add(word)
                completed = True
        except OSError as ose:
            print(ose)
        except Exception as e:
            print(traceback.format_exc())
        finally:
            return word_counter, verse_counter, len(unique_words), completed, formatted_lines

    @staticmethod
    def evaluate_theo_min_nbits(bits : List[int], n_elements : int = 0):
        prfps = {"BvP" : dict.fromkeys(bits)}
        curr_prfp = 1
        for bit in bits:
            fph = FingerprintHandler(n_bits=bit, n_elements=n_elements)
            prfps["BvP"][bit] = fph.prfp
            if fph.prfp < curr_prfp:
                curr_prfp = fph.prfp
                max_bits = bit 
        return prfps, curr_prfp, max_bits
        
