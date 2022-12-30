import string
import re
import os
import traceback

from tqdm import tqdm
from pympler import asizeof as ao

from typing import *

class Tokenizer():
    def __init__(self, log_filename : str = "formatted_verses.txt", log_filepath : str = "log/", gram_filename : str = "sentences.txt", token_length : int = 6):
        self.allowed_chars = ["'"]
        self.SPECIAL_CHARACTERS = [x for x in string.punctuation if x not in self.allowed_chars]
        self.log_filepath = log_filepath
        self.log_filename = log_filename
        self.gram_filename = gram_filename
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

    def build_xgrams(self, unigrams : List[str] = None) -> Tuple[bool, Set[str], float, int, float]:
        """
        This function takes care of the tokenization of the full text. Since we want to build 4-grams and 8-grams
        the output of this function will be a list of strings of lenght 4 and 8, according to the specific instance of this class
        attribute value for self.token_length.
        """
        completed = False
        xgrams = set()
        # num_sentences_generated = len(unigrams)
        num_sentences_generated = 0
        sentence_size = .0
        try:
            sliding_idx = 0
            for _ in tqdm(range(len(unigrams))):
                xgram = [gram for gram in unigrams[sliding_idx:sliding_idx+self.token_length]]
                if " " in xgram:
                    xgram.remove(" s")
                _curr_sentence = ' '.join(xgram)
                if len(xgram) == self.token_length:
                    xgrams.add(_curr_sentence)
                    sentence_size += ao.asizeof(_curr_sentence)
                    sliding_idx += 1
                    num_sentences_generated += 1
            completed = True
        except Exception as e:
            print(traceback.format_exc())
        finally:
            return completed, xgrams, ao.asizeof(xgrams), num_sentences_generated, sentence_size/len(xgrams)

    def log_xgrams(self, grams : Set[str] = None) -> bool:
        completed = False
        try:
            if grams is not None:
                with open(f"{os.path.join(self.log_filepath, self.gram_filename)}", "w") as logf:
                    for gram in grams:
                        logf.write(gram + "\n")
                completed = True
            else:
                raise Exception
        except Exception as e:
            print(traceback.format_exc())
        finally:
            return completed