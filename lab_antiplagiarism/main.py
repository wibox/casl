import string

from typing import *

SPECIAL_CHARACTERS = string.punctuation

unique_words = set()

def clean_text(text : str) -> str:
    for special_char in SPECIAL_CHARACTERS:
        text.replace(special_char, "")
    return text

def retrieve_sentences(text : str) -> List[str]:
    sliding_idx = 0
    sentences = list()
    sentence = list()

    text.replace("\n", "")
    sentence = [text.split(" ")[sliding_idx+i] for i in range(4)]
    sentences.append(sentence)
    sliding_idx += 1
    return sentences


if __name__ == "__main__":

    with open("divina_commedia.txt", "r", encoding="UTF-8") as divina_commedia:
        word_counter = 0
        verse_counter = 0
        lines = divina_commedia.readlines()
        for line in lines:
            #clean each line
            line = clean_text(line)
            #count #verses
            verse_counter += 1
            #count #words
            word_counter += len(line.split(" "))
            #count #unique words
            for word in line.split(" "):
                if word != "":
                    unique_words.add(word)

    print(f"Total number of words: {word_counter}")
    print(f"Total number of verses: {verse_counter}")
    print(f"Total number of distinc words: {len(unique_words)}")