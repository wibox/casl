from tokenizer import Tokenizer

import traceback

from typing import *

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
