from typing import *
from utils import *
import argparse
import os

from pympler import asizeof as ao

if __name__ == "__main__":

    TOKEN_LENGTH = [4, 8]
    N_BITS = [2*i for i in range(1, 33)] # from 16 bit up to 32 (given the amount of stored sentences it has no meaning going lower that 16 -> Pr[FP] approx. 1 )
    myTokenizer = Tokenizer(
            log_filename="formatted_verses.txt",
            log_filepath="log/"
        )
    # COMPUTING REQUESTED QUANTITIES AND LOGGING CLEANED VERSES
    words_counter, verses_counter, unique_words, computation_completed, formatted_lines = compute_text_info(filename="divina_commedia.txt", tokenizer=myTokenizer)
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
            print(f"Number of sentences generated: {num_grams}")
            print(f"Number of sentences in set (unique sentences): {len(grams)}")
            print(f"Memory occupancy of pure strings: {ao.asizeof(grams)/1024:.2f} kilobytes")
            # print(f"Memory occupancy of fingerprints: {ao.asizeof(compute_fingerprints_statistics(grams=grams, num_elements=len(grams), fp_prob=1))/1024} bytes")
            print(f"Logging {token_length}grams in {os.path.join(myTokenizer.log_filepath, myTokenizer.log_filename)}...")
            myTokenizer.log_xgrams(grams=grams)
        
        total_memory = list() # total memory employed for storing all the fingerprints
        fingerprint_size = list() # size (bytes) for single fingerprint
        prob_fp = list()
        for bits in N_BITS:

            myFingerPrintHandler = FingerprintHandler(
                log_filename=f"{bits}_bits_{token_length}_length_fp.txt",
                log_filepath="log/",
                n_bits=bits,
                n_elements=len(grams)
            )

            print(f"Building fingerprints using {bits} bits")
            print(f"\tFingerprint range: {pow(2, bits)-1}")
            print(f"\tCorresponding Pr[FP] = {myFingerPrintHandler.prfp}")

            build_fingerprints, fingerprints, bytes, total_memory_instance = myFingerPrintHandler.build_fingerprints(grams=grams)
            if build_fingerprints:
                total_memory.append(total_memory_instance / 1024)
                print(f"\tTotal memory employed: {total_memory_instance}")
                fingerprint_size.append(bytes)
                print(f"\tMemory used to store one fingerprint: {bytes}")
                prob_fp.append(myFingerPrintHandler.prfp)
                # myFingerPrintHandler.log_fingerprints(fingerprints=fingerprints)
            del myFingerPrintHandler

        plot_results(
            x = prob_fp,
            y = total_memory,
            #thr=os.stat(f"log/{token_length}grams.txt").st_size,
            thr=ao.asizeof(grams)/1024,
            xscale='log',
            yscale='linear',
            xlabel="False-Positive probability",
            ylabel="Total Memory (kilobytes)",
            title=f"{token_length}grams - Fingerprints' total memory vs Pr[FP]",
            filename=f"{token_length}_tmprob.png",
        )

        plot_results(
            x = prob_fp,
            y = fingerprint_size,
            xscale='log',
            yscale='linear',
            xlabel="False-Positive probability",
            ylabel="Fingerprint size (bytes)",
            title=f"{token_length}grams - Fingerprints' size (bytes) vs Pr[FP]",
            filename=f"{token_length}_fsprob.png",
        )
        