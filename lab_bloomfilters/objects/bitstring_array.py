from .utils import Helper

import numpy as np

from typing import *

class BitStringArray():
    def __init__(
            self,
            log_filepath : str,
            log_filename : str,
            bits : List[int],
            sentences : Set[str]
        ):
        self.log_filepath = log_filepath
        self.log_filename = log_filename
        self.bits = bits
        self.sentences = sentences

    def _initialise_bsa(self, range : int) -> np.ndarray:
        return np.zeros(range)

    def theo_prfp(self) -> List[float]:
        theo_prfps = list()
        if len(self.sentences) > 0:
            for bit in self.bits:
                theo_prfps.append(1 - pow(1 - (1/(pow(2, bit)-1)), len(self.sentences)))
            return theo_prfps
        else:
            raise Exception(f"Please provide a few more elements. Found: {len(self.sentences)}")

    def simulate_prpf(self) -> Tuple[List[float], List[float]]:
        prfp = list()
        collisions_list = list()
        for bit in self.bits:
            dimension = pow(2, bit)
            print(f"\tStoring fingerprints using 2^{bit}={dimension} bits")
            bsa = self._initialise_bsa(range=dimension)
            collisions = 0
            for sentence in self.sentences:
                _fp = Helper.compute_hash(sentence=sentence, bits=bit)
                if bsa[_fp] == 1:
                    collisions += 1
                else:
                    bsa[_fp] = 1
            prfp.append(np.sum(bsa)/dimension)
            collisions_list.append(collisions)
            print(f"\t\tFound {collisions} collisions")
        return prfp, collisions_list