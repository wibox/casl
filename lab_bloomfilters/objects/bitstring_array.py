from .fingerprint_handler import FingerprintHandler

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

    def compute_theo_prfp(self):
        pass

    def simulate_prpf(self) -> Tuple[List[float], List[float]]:
        prfp = list()
        collisions_list = list()
        for bit in self.bits:
            print(f"Storing fingerprints using {pow(2, bit)} bits")
            bsa = self._initialise_bsa(range=pow(2, bit))
            fph = FingerprintHandler(n_bits=bit, n_elements=len(self.sentences))
            collisions = 0
            for sentence in self.sentences:
                _fp = fph._fp(sentence=sentence)
                if bsa[_fp] == 1:
                    collisions += 1
                else:
                    bsa[_fp] = 1
            prfp.append(np.sum(bsa)/pow(2, bit))
            collisions_list.append(collisions)
            print(f"\tFound {collisions} collisions")
        return prfp, collisions_list