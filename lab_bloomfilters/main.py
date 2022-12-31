from objects.tokenizer import Tokenizer
from objects.fingerprint_handler import FingerprintHandler
from objects.bitstring_array import BitStringArray
from objects.bloom_filter import BloomFilter
from objects.utils import Helper, Constants
from objects.parser import custom_parser

import os

if __name__ == "__main__":
    args = custom_parser()

    myTokenizer = Tokenizer(
                    log_filename=Constants.FORMATTED_TEXT_FILENAME,
                    log_filepath=Constants.LOG_FOLDER_PATH,
                    gram_filename=Constants.GRAM_FILENAME,
                    token_length=Constants.GRAM_SIZE
                )

    # computing initial quantities
    words_counter, verses_counter, unique_words, computation_completed, formatted_lines = Helper.compute_text_info(filename="divina_commedia.txt", tokenizer=myTokenizer)
    log_completed = myTokenizer.log_formatted_verses(formatted_lines)
    
    if log_completed:
        print(f"Logged formatted verses in: {os.path.join(myTokenizer.log_filepath, myTokenizer.log_filename)}")
    
    if computation_completed:
        print("Informations retrieved from selected text:")
        print(f"\t Total number of words: {words_counter}")
        print(f"\t Total number of verses: {verses_counter}")
        print(f"\t Total number of distinc words: {unique_words}")
        print(f"\t Whole formatted file takes: {os.path.getsize(os.path.join(Constants.LOG_FOLDER_PATH, Constants.FORMATTED_TEXT_FILENAME))/1024:.1f} kilobytes")

    load_completed, unigrams = myTokenizer.load_formatted_text(filename=os.path.join(Constants.LOG_FOLDER_PATH, Constants.FORMATTED_TEXT_FILENAME))
    if load_completed:
        print("Loaded unigrams from formatted text.")

    print(f"Building {Constants.GRAM_SIZE}grams...")

    build_grams, grams, grams_occupancy, num_grams, avg_gram_occupancy = myTokenizer.build_xgrams(unigrams=unigrams)
    if build_grams:
        print(f"Number of sentences generated: {num_grams}")
        print(f"Number of sentences in set (unique sentences): {len(grams)}")
        print(f"Set's memory occupancy: {grams_occupancy/1024:.1f} kilobytes")
        print(f"Average memory occupancy of each sentence: {avg_gram_occupancy:.2f} bytes")
        print(f"Logging {Constants.GRAM_SIZE}grams in {os.path.join(myTokenizer.log_filepath, myTokenizer.gram_filename)}...")
        myTokenizer.log_xgrams(grams=grams)

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

    print("Stroring sentences using a BitString Array")
    bsa_bits = [i for i in range(19, 24)]
    bsa = BitStringArray(
            log_filepath=Constants.PLOT_FOLDER_PATH,
            log_filename=Constants.BSA_FILENAME,
            bits=bsa_bits,
            sentences=grams
        )
    prfp, collisions = bsa.simulate_prpf()
    Helper.plot_results(
        y = [prfp, collisions],
        x = [[pow(2, bit) for bit in bsa_bits], [pow(2, bit) for bit in bsa_bits]],
        xlabel= ["Bits used", "Bits used"],
        ylabel = ["Pr[FP]", "Collisions found"],
        ax_title = ["Probability of false positive in function of bits", "Collisions found in function of bits"],
        fig_title = "BitString Array behaviour in function of memory occupancy",
        save_fig_bool = True,
        filepath = Constants.PLOT_FOLDER_PATH,
        filename = "bsa.png"
    )
