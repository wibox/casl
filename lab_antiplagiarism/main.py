from typing import *
from utils import *
import argparse
import os

from pympler import asizeof as ao

if __name__ == "__main__":

    TOKEN_LENGTH = [4, 8]
    FP_PROBS = [pow(10, -i) for i in range(10)]
    myTokenizer = Tokenizer(
            log_filename="formatted_verses.txt",
            log_filepath="log/"
        )
    # COMPUTING REQUESTED QUANTITIES AND LOGGING CLEANED VERSES
    words_counter, verses_counter, unique_words, computation_completed, formatted_lines = compute_statistics(filename="divina_commedia.txt", tokenizer=myTokenizer)
    log_completed = myTokenizer.log_formatted_verses(formatted_lines)
    if log_completed:
        print(f"Logged formatted verses in: {os.path.join(myTokenizer.log_filepath, myTokenizer.log_filename)}")

    if computation_completed:
        print("\n Informations retrieved from selected text:")
        print(f"\t Total number of words: {words_counter}")
        print(f"\t Total number of verses: {verses_counter}")
        print(f"\t Total number of distinc words: {unique_words}")
        print(f"\t Whole unformatted file takes: {os.path.getsize('divina_commedia.txt')/1024} kilobytes")

    # START TOKENIZATION AND FINGERPRINTING
    print(f"\nBUILDING TOKENS WITH LENGTHS 4 AND 8...")

    for token_length in TOKEN_LENGTH:
        print(f"\t=====Working with {token_length}grams=====")

        myTokenizer = Tokenizer(
            log_filename=f"{token_length}grams.txt",
            log_filepath="log/",
            token_length=token_length
        )

        load_completed, unigrams = myTokenizer.load_formatted_text(filename="log/formatted_verses.txt")
        if load_completed:
            print("Loaded unigrams from formatted text.")

        print(f"Building {token_length}grams...")

        build_grams, grams, num_grams = myTokenizer.build_xgrams(unigrams=unigrams)
        if build_grams:
            print(f"Number of sentences stored: {num_grams}")
            print(f"Memory occupancy of pure strings: {ao.asizeof(grams)/1024} kilobytes")
            print(f"Memory occupancy of fingerprints: {ao.asizeof(compute_fingerprints_statistics(grams=grams, num_elements=len(grams), fp_prob=1e-7))} bytes")
            print(f"Logging {token_length}grams in {os.path.join(myTokenizer.log_filepath, myTokenizer.log_filename)}...")
            myTokenizer.log_xgrams(grams=grams)