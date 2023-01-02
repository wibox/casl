from .utils import Helper

import numpy as np

from typing import *

class BloomFilter():
    def __init__(
        self,
        log_filepath : str,
        log_filename : str,
        bits : List[int],
        sentences : Set[str],
        opt_k : List[int]
    ):
        self.log_filepath = log_filepath
        self.log_filename = log_filename
        self.bits = bits
        self.sentences = sentences
        self.opt_k = opt_k

    def _initialise_bf(self, range : int) -> np.ndarray:
        return np.zeros(range)

    def _count_theo_inserted_elements(self, hashes : int, bits : int, bloom_filter : np.ndarray) -> int:
        return - pow(2, bits)/hashes * np.log(1 - np.sum(bloom_filter)/pow(2, bits))

    def _build_subsentences(self, modifiers : List[str], sentence : str) -> List[str]:
        sub_sentences = list()
        for modifier in modifiers:
            sub_sentences.append(sentence + modifier)
        return sub_sentences

    def _add_element_and_check_for_conflicts(self, bloom_filter : np.ndarray, indexes : List[int]) -> Tuple[np.ndarray, bool]:
        _count = 0
        for index in indexes:
            if bloom_filter[index] == 1:
                _count += 1
            else:
                bloom_filter[index] = 1
        if _count == len(indexes):
            return bloom_filter, True
        else:
            return bloom_filter, False

    def theo_prfp(self, hashes : int = 5) -> List[float]:
        theo_prfp = list()
        for bit in self.bits:
            theo_prfp.append(pow(1-np.exp(-(hashes*len(self.sentences))/(pow(2, bit)-1)), hashes))
        return theo_prfp

    def simulate_prfp(self) -> Tuple[List[float], List[float]]:
        prfp = list()
        collisions_list = list()
        for bit, k in zip(self.bits, self.opt_k):
            modifiers = [str(rnd) for rnd in range(k)]
            dimension = pow(2, bit)
            print(f"\tStoring fingerprints using 2^{bit}={dimension} bits. Hash functions: {k}")
            bf = self._initialise_bf(range=dimension)
            collisions = 0
            added_elements = 0
            for sentence in self.sentences:
                hashed_sentence = self._build_subsentences(modifiers=modifiers, sentence=sentence)
                indexes = list()
                for sub_sentence in hashed_sentence:
                    _fp = Helper.compute_hash(sentence=sub_sentence, bits=bit)
                    indexes.append(_fp)
                bf, conflict_found = self._add_element_and_check_for_conflicts(bloom_filter=bf, indexes=indexes)
                if conflict_found:
                    collisions += 1
                else:
                    added_elements += 1
            collisions_list.append(collisions)
            prfp.append(collisions/dimension)
            print(f"\t\tFound {collisions} collisions")
            print(f"\t\tInserted {added_elements} elements without any conflict.")
            print(f"\t\tTheory allows {self._count_theo_inserted_elements(hashes=k, bloom_filter=bf, bits=bit)} to be inserted.")
        
        return prfp, collisions_list
