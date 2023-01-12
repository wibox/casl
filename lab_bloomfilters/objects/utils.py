from .tokenizer import Tokenizer
from .fingerprint_handler import FingerprintHandler

import matplotlib.pyplot as plt

import traceback
import hashlib
import json
import os

from typing import *

class Constants:
    """
    Wrapper class around useful constants for the proper functioning of the whole simulator.
    """
    LOG_FOLDER_PATH = "log/"
    PLOT_FOLDER_PATH = "plots/"
    FORMATTED_TEXT_FILENAME = "formatted_verses.txt"
    GRAM_FILENAME = "grams.txt"
    GRAM_SIZE = 6
    FP_FILENAME = "fp.txt"
    PRFPS_FILENAME = "prfps.txt"
    BSA_FILENAME = "bsa.txt"
    BF_FILENAME = "bf.txt"

class Helper:
    """
    Static class to wrap utility routines.
    """
    @staticmethod
    def format_output(width : int) -> None:
        """
        Prints text formatting information to stdout in order to make logging more clear.
        Args:
            - width : int -> Width of the separator line to be printed; used: os.get_terminal_size()[0]
        """
        for _ in range(width):
            print("=", end="")

    @staticmethod
    def compute_hash(sentence : str, bits : int) -> int:
        """
        Returns the hash of a given sentence using a fixed number of bits
        Args:
            - sentnece : str -> the sentence for which hash has to be built
            - bits : int -> number of bits to use for the encoding
        Returns:
            - int -> computed hash for the input sentence with given number of bits
        """
        n = pow(2, bits) - 1 # defining hash range in function of allowed bits
        # building hash using hashlib's implementation of md5
        return int(hashlib.md5(sentence.encode('utf-8')).hexdigest(), 16) % n

    @staticmethod
    def plot_results(
        x : List[List[float]],
        y : List[List[List[float]]],
        legend_handles : List[List[str]],
        category : str,
        xlabel : List[str],
        ylabel : List[str],
        ax_title : List[str],
        fig_title : str,
        save_fig_bool : bool,
        filepath : str,
        filename : str,
        close_fig_bool : bool = True
    ) -> None:
        """
        Perform the plot of inputs arrays into a proper, user-decided format.
        Args:
            - x : List[List[float]] -> nested lists to be plotted on same ax if _dim > 1
            - y : List[List[List[float]]]  -> nested lists to be plotted on different axis if _dim > 1
            - legend_handles : List[List[str]] -> legend handles for each ax
            - category : str -> placeholder value for logging images
            - xlabel : List[str] -> xlabel for ax
            - ylabel : List[str] -> ylabel for ax
            - ax_title : List[str] -> title for ax
            - fig_title : str -> fig suptitle
            - save_fig_bool : bool -> decides if either save or not the final picture. mainly used for debugging purposes
            - filepath : str -> filepath in which picture should be logged
            - filename : str -> filename for saved picture
            - close_fig_bool : bool = True -> wheather to close the fig while plotting to keep adding plots to ax or not, mainly used for debugging
        """
        assert len(x) == len(y), "Size mismatch in input."
        num_plots = len(y)
        if num_plots > 1: # if more than one List[float] is passed, fig is divided into [1, num_plots] axis
            fig, axs = plt.subplots(1, num_plots, figsize=(6*num_plots, 5)) # defining fig_size
            fig.suptitle(fig_title) # setting fig title
            # iterating through every generated ax to plot corresponding informations contained in x and y.
            for x_el, y_el, legend_handle, xlabel_el, ylabel_el, title_el, idx in zip(x, y, legend_handles, xlabel, ylabel, ax_title, range(num_plots)):
                axs[idx].grid() # set grid for each ax
                for sub_y, sub_handle in zip(y_el, legend_handle): # iterate through every graph to put in each ax
                    axs[idx].plot(x_el, sub_y, linestyle="--", marker='o', label=sub_handle) # plotting informations
                    axs[idx].set_xlabel(xlabel_el) # setting xlabel
                    axs[idx].set_ylabel(ylabel_el) # setting ylabel
                    axs[idx].set_title(title_el) # setting ax title
                    axs[idx].legend() # activating legend with input:legend_handles
        else: # if just one List[float] is passed
            fig, ax = plt.subplots(figsize=(6, 5)) # define standard subplots dimensions
            fig.suptitle(fig_title) # setting fig title
            ax.plot(x[0], y[0][0], linestyle="--", marker='o', label=legend_handles[0][0]) # plotting informations
            ax.grid() # setting grid for ax
            ax.set_xlabel(xlabel[0]) # setting xlabel
            ax.set_ylabel(ylabel[0]) # setting ylabel
            ax.set_title(ax_title[0]) # setting ax title
            ax.legend() # activating legend with input:legend_handles

        if save_fig_bool:
            # save fig and close plotting routine if specified 
            print(f"Saving picture with informations about {category} in {os.path.join(filepath, filename)}")
            plt.savefig(os.path.join(filepath, filename))
            if close_fig_bool:
                plt.close()

    @staticmethod
    def log_json(filename : str, filepath : str, json_obj : Dict[int, float] = None) -> bool:
        """
        Logs json_obj to a json formatted file.
        Args:
            - filename : str -> name for the output filename
            - fileapth : str -> logging path reference
            - json_obj : Dict[int, float] -> python dictionary to be logged
        Returns:
            - bool -> either if logging operation was successful or not
        """
        completed = False
        try:
            with open(os.path.join(filepath, filename), "w") as outds:
                json.dump(json_obj, outds, indent=4)
            completed = True # boolean output defined in function of operation's success
        except Exception as e:
            print(traceback.format_exc()) # catching eveyr general exception throwed
        finally:
            return completed # returning logging operation's success

    @staticmethod
    def compute_text_info(filename : str = "divina_commedia.txt", tokenizer : Tokenizer = Tokenizer()) -> Tuple[int, int, int, bool, List[str]]:
        """
        Computes info statistics about the input filename.
        Args:
            - filename : str -> input filename to be processed
            - tokenizer : Tokenizer -> specific Type[Tokenizer] object employed in formatting the output sentences
        Returns:
            - int -> counter for the total words in the input text
            - int -> counter for the total number of verses in the input text
            - int -> counter for unique words found in input text
            - bool -> wheather if formatting operation was successful or not
            - List[str] -> formatted lines from original text
        """
        completed = False # boolean to judge wheater operation was successful or not
        unique_words = set() # empty set initialization in which unique words will be inserted
        formatted_lines = list() # empty list initialization in which formatted sentences will be inserted
        word_counter = 0 # total words counter
        verse_counter = 0 # total verses counter
        try:
            with open(f"{filename}", "r") as divina_commedia:
                lines = divina_commedia.readlines() #reading lines from input text
                for line in lines: # iterating through each line
                    line = tokenizer.clean_line(line) # clean each line
                    formatted_lines.append(line) # insert formatted line in method's output
                    if line != "":
                        verse_counter += 1 # increasing verse counter if formatting didn't produced an empty string
                    word_counter += len(line.split(" ")) # updating total words counter which lenght of current sentece
                    for word in line.split(" "):
                        unique_words.add(word) # adding a new unique words from sentence words' list
                completed = True # if overall operation was successful, return True
        except OSError as ose: # catching OSError if filename can not be accesses
            print(ose)
        except Exception as e: # catching any other general expression
            print(traceback.format_exc())
        finally:
            # eventually, return counters, operation's success and formatted verses
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
        
