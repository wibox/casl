import string
import re
import os
import traceback
import hashlib

from typing import *

import matplotlib.pyplot as plt

from tqdm import tqdm
from pympler import asizeof as asof

class FingerprintHandler():
    def __init__(self, log_filename : str = None, log_filepath : str = None, n_bits : int = 16, n_elements : int = 0):
        self.log_filename = log_filename
        self.log_filepath = log_filepath
        self.n_bits = n_bits
        self.n_elements = n_elements
        self.prfp = self._compute_prfp()

    def _compute_prfp(self) -> float:
        if self.n_elements > 0:
            return 1 - pow(1 - (1/(pow(2, self.n_bits)-1)), self.n_elements)
        else:
            raise Exception(f"Please provide a few more elements. Found: {self.n_elements}")

    def _compute_fp_range(self) -> int:
        return pow(2, self.n_bits) - 1 

    def _fp(self, sentence : str = None) -> int:
        """
        This function returns the fingerprint of an input string in the range [0, n-1]
        """
        n = self._compute_fp_range()
        return int(hashlib.md5(sentence.encode('utf-8')).hexdigest(), 16) % n

    def build_fingerprints(self, grams : Set[str] = None) -> Tuple[bool, Set[int], float, float]:
        completed = False
        fingerprints = set()
        try:
            if grams:
                for gram in grams:
                    fingerprints.add(self._fp(sentence=gram))
                completed = True
        except Exception as e:
            print(e.format_exc())
        finally:
            return completed, fingerprints, self.n_bits/8, asof.asizeof(fingerprints)
    
    def log_fingerprints(self, fingerprints : Set[int] = None) -> bool:
        completed = False
        try:
            if fingerprints:
                with open(f"{os.path.join(self.log_filepath, self.log_filename)}", "w") as fp:
                    for fingerprint in fingerprints:
                        fp.write(str(fingerprint) + "\n")
                completed = True
        except Exception as e:
            print(e.format_exc())
        finally:
            return completed

class Tokenizer():
    def __init__(self, log_filename : str = None, log_filepath : str = "log/", token_length : int = 4):
        self.allowed_chars = ["'"]
        self.SPECIAL_CHARACTERS = [x for x in string.punctuation if x not in self.allowed_chars]
        self.log_filepath = log_filepath
        self.log_filename = log_filename
        self.token_length = token_length

    def clean_line(self, verse : str) -> str:
        # removing useless line
        USELESS_LINES = ["inferno", "purgatorio", "paradiso", "la divina commedia", "di dante alighieri"]
        # removing punctuation
        for special_char in self.SPECIAL_CHARACTERS:
            verse = verse.replace(special_char, '')
        # removing headers
        for useless_line in USELESS_LINES:
            if verse.lower().startswith(useless_line):
                verse = ""
        return verse

    def log_formatted_verses(self, verses : List[str]) -> bool:
        completed = False
        try:
            with open(f"{os.path.join(self.log_filepath, self.log_filename)}", "w") as formatted_verses:
                for verse in verses:
                    if verse not in [" ", "\n", ""]:
                        formatted_verses.write(re.sub(' +', ' ', verse.strip()) + " ")
            completed = True
        except Exception as e:
            print(traceback.format_exc())
        finally:
            return completed

    def load_formatted_text(self, filename : str = None) -> Tuple[bool, Union[List[str], None]]:
        completed = False
        try:
            with open(filename, "r") as tl: # to-load
                unigrams = tl.read().split(" ")
            completed = True
        except Exception as e:
            print(traceback.format_exc())
        finally:
            return completed, unigrams

    def build_xgrams(self, unigrams : List[str] = None) -> Tuple[bool, Set[str], int]:
        """
        This function takes care of the tokenization of the full text. Since we want to build 4-grams and 8-grams
        the output of this function will be a list of strings of lenght 4 and 8, according to the specific instance of this class
        attribute value for self.token_length.
        """
        completed = False
        xgrams = set()
        # num_sentences_generated = len(unigrams)
        num_sentences_generated = 0
        try:
            sliding_idx = 0
            for _ in tqdm(range(len(unigrams))):
                xgram = [gram for gram in unigrams[sliding_idx:sliding_idx+self.token_length]]
                if " " in xgram:
                    xgram.remove(" s")
                _curr_sentence = ' '.join(xgram)
                if len(xgram) == self.token_length:
                    xgrams.add(_curr_sentence)
                    sliding_idx += 1
                    num_sentences_generated += 1
            completed = True
        except Exception as e:
            print(traceback.format_exc())
        finally:
            return completed, xgrams, num_sentences_generated

    def log_xgrams(self, grams : Set[str] = None) -> bool:
        completed = False
        try:
            if grams is not None:
                with open(f"{os.path.join(self.log_filepath, self.log_filename)}", "w") as logf:
                    for gram in grams:
                        logf.write(gram + "\n")
                completed = True
            else:
                raise Exception
        except Exception as e:
            print(traceback.format_exc())
        finally:
            return completed

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

def plot_results(x : List[float], y : List[int], xscale : str, yscale : str, xlabel : str, ylabel : str, title : str, filename : str, thr : int = None, filepath : str = "results/", save_fig_bool : bool = True):
    
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(x, y)
    if thr:
        ax.axhline(y=thr, color='r', linestyle='dotted')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xscale(xscale)
    ax.set_yscale(yscale)
    if save_fig_bool:
        plt.savefig(os.path.join(filepath, filename))