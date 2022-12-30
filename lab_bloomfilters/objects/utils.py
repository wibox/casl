from .tokenizer import Tokenizer
from .fingerprint_handler import FingerprintHandler

from pympler import asizeof as ao

import traceback
import json
import os

from typing import *

class Constants:

    LOG_FOLDER_PATH = "log/"
    
    FORMATTED_TEXT_FILENAME = "formatted_verses.txt"
    
    GRAM_FILENAME = "grams.txt"
    GRAM_SIZE = 6

    FP_FILENAME = "fp.txt"

    PRFPS_FILENAME = "prfps.txt"

class Helper:

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
        
