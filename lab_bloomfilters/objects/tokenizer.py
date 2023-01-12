import string
import re
import os
import traceback

from tqdm import tqdm
from pympler import asizeof as ao

from typing import *

class Tokenizer():
    """
    Class responsible for sentence cleaning and tokenization
    Args:
        - log_filename : str -> filename for produced log files
        - log_filepath : str -> filepath for produced log files
        - gram_filename : str -> filename for lenght-6 clean sentences produced
        - token_lenght : int -> lenght of built clean sentences
    """
    def __init__(
        self,
        log_filename : str = "formatted_verses.txt",
        log_filepath : str = "log/",
        gram_filename : str = "sentences.txt",
        token_length : int = 6
    ):
        self.allowed_chars = ["'"] # allowing specific list of characters which could impact text's meaning
        # defining characters to be removed from standard set of puncutuation if each character is not in self.allowed_chars
        self.SPECIAL_CHARACTERS = [x for x in string.punctuation if x not in self.allowed_chars]
        self.log_filepath = log_filepath # setting class's properties
        self.log_filename = log_filename # setting class's properties
        self.gram_filename = gram_filename # setting class's properties
        self.token_length = token_length # setting class's properties

    def clean_line(self, verse : str) -> str:
        """
        Cleans the line with a specific criterion tailored around divina_commedia.txt
        Args:
            - verse : str -> original verse to be cleaned
        """
        # removing useless lines
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
        """
        Logs clean verses in specified path
        Args:
             - verses : List[str] -> list of formatted verses produced by self
        """
        completed = False # operation's output boolean variable
        try:
            with open(f"{os.path.join(self.log_filepath, self.log_filename)}", "w") as formatted_verses:
                for verse in verses: # iterating throguh each formatted verse
                    if verse not in [" ", "\n", ""]:
                        formatted_verses.write(re.sub(' +', ' ', verse.strip()) + " ")
            completed = True # setting to True if logging's was successful
        except Exception as e: # catching any general throwed exceptions
            print(traceback.format_exc())
        finally:
            # eventually return operation's output
            return completed

    def load_formatted_text(self, filename : str = None) -> Tuple[bool, Union[List[str], None]]:
        """
        Logs formatted verses in specified logpath
        Args:
            - filename : str -> filename for logfile
        Returns:
            - bool -> operation's success
            - List[str] ->  list of sentences stored from logfile
        """
        completed = False
        unigrams = list()
        try:
            with open(filename, "r") as tl: # to-load
                unigrams.extend(tl.read().split(" ")) # reading each line as a list of space-separated words
            completed = True
        except Exception as e: # catching every general expression
            print(traceback.format_exc())
        finally:
            # eventually return loading success and outputs
            return completed, unigrams

    def build_xgrams(self, unigrams : List[str] = None) -> Tuple[bool, Set[str], float, int, float]:
        """
        Takes care of the tokenization of the full text.
        Args:
            - unigrams : List[str] -> list of sentences used to build lenght-6 sentences
        Returns:
            - bool -> operation's success
            - Set[str] -> Set containing 6grams
            - float -> byte-wise dimension of 6grams' set
            - int -> number of generated sentences
            - float -> average size of each sentence in bytes
        """
        completed = False # operation's success
        xgrams = set() # set of lenght-6 sentences
        num_sentences_generated = 0 # counter of the number of lenght-6 sentences
        sentence_size = .0 # float counter of average 6gram size in bytes
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