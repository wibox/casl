from objects.tokenizer import Tokenizer
from objects.fingerprint_handler import FingerprintHandler
from objects.bitstring_array import BitStringArray
from objects.bloom_filter import BloomFilter
from objects.utils import Helper, Constants
from objects.parser import custom_parser

import os

import math

if __name__ == "__main__":
    args = custom_parser()

    myTokenizer = Tokenizer(
                    log_filename=Constants.FORMATTED_TEXT_FILENAME,
                    log_filepath=Constants.LOG_FOLDER_PATH,
                    gram_filename=Constants.GRAM_FILENAME,
                    token_length=Constants.GRAM_SIZE
                )

    # computing initial quantities
    print(f"Performing preprocessing over {args.filename}...")
    words_counter,\
         verses_counter,\
             unique_words,\
                 computation_completed,\
                     formatted_lines = Helper.compute_text_info(filename="divina_commedia.txt", tokenizer=myTokenizer)
    log_completed = myTokenizer.log_formatted_verses(formatted_lines)
    
    if log_completed:
        print(f"Logged formatted verses in: {os.path.join(myTokenizer.log_filepath, myTokenizer.log_filename)}")
        Helper.format_output(width=os.get_terminal_size()[0])
    
    if computation_completed:
        print("Informations retrieved from selected text:")
        print(f"\t Total number of words: {words_counter}")
        print(f"\t Total number of verses: {verses_counter}")
        print(f"\t Total number of distinc words: {unique_words}")
        print(f"\t Whole formatted file takes: {os.path.getsize(os.path.join(Constants.LOG_FOLDER_PATH, Constants.FORMATTED_TEXT_FILENAME))/1024:.1f} kilobytes")
        Helper.format_output(width=os.get_terminal_size()[0])

    load_completed, unigrams = myTokenizer.load_formatted_text(
            filename=os.path.join(Constants.LOG_FOLDER_PATH, Constants.FORMATTED_TEXT_FILENAME)
        )
    if load_completed:
        print("Loaded unigrams from formatted text.")

    print(f"Building {Constants.GRAM_SIZE}grams...")

    build_grams,\
         grams,\
             grams_occupancy,\
                 num_grams,\
                     avg_gram_occupancy = myTokenizer.build_xgrams(unigrams=unigrams)
    if build_grams:
        print(f"Number of sentences generated: {num_grams}")
        print(f"Number of sentences in set (unique sentences): {len(grams)}")
        print(f"Set's memory occupancy: {grams_occupancy/1024:.1f} kilobytes")
        print(f"Average memory occupancy of each sentence: {avg_gram_occupancy:.2f} bytes")
        print(f"Logging {Constants.GRAM_SIZE}grams in {os.path.join(myTokenizer.log_filepath, myTokenizer.gram_filename)}...")
        myTokenizer.log_xgrams(grams=grams)
        Helper.format_output(width=os.get_terminal_size()[0])

    myFingerprintHandler = FingerprintHandler(
                                log_filename=Constants.FP_FILENAME,
                                log_filepath=Constants.LOG_FOLDER_PATH,
                                n_elements=num_grams
                        )
    print("Computing minimum number of bits to achieve zero conflicts for fingerprints (prpf=0)...")
    fph_bits = [2*i for i in range(1, 33)]
    prfps, best_prfp, max_bits_fph = Helper.evaluate_theo_min_nbits(n_elements=num_grams, bits=fph_bits)
    print(f"\tBest probability found: {best_prfp}")
    print(f"\tCorresponding number of bits: {max_bits_fph}")
    print(f"\tLogging probabilities and corresponding bits in {os.path.join(Constants.LOG_FOLDER_PATH, Constants.PRFPS_FILENAME)}...")
    
    Helper.log_json(filepath=Constants.LOG_FOLDER_PATH, filename=Constants.PRFPS_FILENAME, json_obj=prfps)
    
    print("Simulating a real behavior:")
    for bit in fph_bits:
        print(f"\tUsing {bit} bits")
        fph = FingerprintHandler(
                log_filename=Constants.FP_FILENAME,
                log_filepath=Constants.LOG_FOLDER_PATH,
                n_bits=bit,
                n_elements=num_grams
            )
        _, conflict_found, fingerprints, hash_bytes, _ = fph.build_fingerprints(grams=grams)
        if conflict_found:
            continue
        else:
            print(f"No conflict experienced using {int(hash_bytes*8)} bits")
            print(f"Corresponding probability to get a false positive: {fph.prfp}")
            print(f"Logging fingerprints in {os.path.join(myFingerprintHandler.log_filepath, myFingerprintHandler.log_filename)}...")
            fph.log_fingerprints(fingerprints=fingerprints)
            break

    Helper.format_output(width=os.get_terminal_size()[0])
    print("Storing sentences using a BitString Array")
    bsa_bits = [i for i in range(19, 24)]
    bsa = BitStringArray(
            log_filepath=Constants.LOG_FOLDER_PATH,
            log_filename=Constants.BSA_FILENAME,
            bits=bsa_bits,
            sentences=grams
        )
    bsa_prfp, bsa_collisions = bsa.simulate_prpf()
    bsa_theo_prfp = bsa.theo_prfp()
    Helper.plot_results(
        y = [[bsa_prfp, bsa_theo_prfp], [bsa_collisions]],
        x = [[pow(2, bit) for bit in bsa_bits], [pow(2, bit) for bit in bsa_bits]],
        legend_handles=[["Pr[FP]", "Pr[FP] theoretic"], ["Collisions"]],
        category="BitString Array",
        xlabel= ["Memory (bits)", "Memory (bits)"],
        ylabel = ["Pr[FP]", "Collisions found"],
        ax_title = ["Probability of false positive in function of memory occupancy", "Collisions found in function of memory occypancy"],
        fig_title = "BitString Array behaviour in function of memory occupancy",
        save_fig_bool = True,
        filepath = Constants.PLOT_FOLDER_PATH,
        filename = "bsa.png"
    )

    Helper.format_output(width=os.get_terminal_size()[0])
    print("Storing sentences using a Bloom Filter")
    bf_bits = bsa_bits
    print("Computing optimal number of hashes in function of memory...")
    bf_hashes = [round((pow(2, n)-1)/len(grams)*math.log(2)) for n in bf_bits]
    Helper.plot_results(
        y = [[bf_hashes]],
        x = [[pow(2, bit) for bit in bf_bits]],
        legend_handles=[["Number of hash functions"]],
        category="optimal number of hash functions",
        xlabel= ["Memory (bits)"],
        ylabel = ["Optimal number of hash functions"],
        ax_title = ["Optimal number of hash functions in function of memory(bits)"],
        fig_title = "Bloom Filter design in function of memory occupancy",
        save_fig_bool = True,
        filepath = Constants.PLOT_FOLDER_PATH,
        filename = "bf_hashes.png"
    )
    bf = BloomFilter(
        log_filepath=Constants.LOG_FOLDER_PATH,
        log_filename=Constants.BF_FILENAME,
        bits=bf_bits,
        sentences=grams,
        opt_k=bf_hashes
        )
    bf_prfp, bf_collisions = bf.simulate_prfp()
    bf_theo_prfp = bf.theo_prfp()
    Helper.plot_results(
        y = [[bf_prfp, bf_theo_prfp], [bf_collisions]],
        x = [[pow(2, bit) for bit in bf_bits], [pow(2, bit) for bit in bf_bits]],
        legend_handles=[["Pr[FP]", "Pr[FP] theoretic"], ["Collisions"]],
        category=f"Bloom Filter",
        xlabel= ["Memory (bits)", "Memory (bits)"],
        ylabel = ["Pr[FP]", "Collisions found"],
        ax_title = ["Probability of false positive in function of bits", "Collisions found in function of bits"],
        fig_title = "Bloom Filter behaviour in function of memory occupancy",
        save_fig_bool = True,
        filepath = Constants.PLOT_FOLDER_PATH,
        filename = "bf.png",
        close_fig_bool=False
    )
