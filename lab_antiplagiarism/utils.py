from typing import *
import string
import re
import os
import traceback

from pympler import asizeof as ao

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

    def build_xgrams(self, unigrams : List[str] = None) -> Tuple[bool, List[str], int]:
        """
        This function takes care of the tokenization of the full text. Since we want to build 4-grams and 8-grams
        the output of this function will be a list of strings of lenght 4 and 8, according to the specific instance of this class
        attribute value for self.token_length.
        """
        completed = False
        xgrams = list()
        xgrams_counter = 0
        try:
            sliding_idx = 0
            num_possible_grams = len(unigrams)//self.token_length + len(unigrams)%self.token_length
            while sliding_idx < num_possible_grams:
                xgram = [gram for gram in unigrams[sliding_idx:sliding_idx+self.token_length]]
                xgrams.append(' '.join(xgram))
                xgrams_counter += 1
                sliding_idx += 1
            completed = True
        except Exception as e:
            print(traceback.format_exc())
        finally:
            return completed, xgrams, xgrams_counter

    def log_xgrams(self, grams : List[str] = None) -> bool:
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

def compute_statistics(filename : str = "divina_commedia.txt", tokenizer : Tokenizer = Tokenizer()) -> Tuple[int, int, int, bool, List[str]]:
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