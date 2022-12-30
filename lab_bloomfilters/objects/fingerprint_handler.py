import os
import hashlib
import traceback

from typing import *

from tqdm import tqdm
from pympler import asizeof as asof

class FingerprintHandler():
    def __init__(self, log_filename : str = None, log_filepath : str = None, n_bits : int = 16, n_elements : int = 0):
        self.log_filename = log_filename
        self.log_filepath = log_filepath
        self.n_bits = n_bits
        self.n_elements = n_elements
        self.prfp = self._compute_prfp()

    def _compute_prfp(self) -> float:
        if self.n_elements > 0:
            return 1 - pow(1 - (1/(pow(2, self.n_bits)-1)), self.n_elements)
        else:
            raise Exception(f"Please provide a few more elements. Found: {self.n_elements}")

    def _compute_fp_range(self) -> int:
        return pow(2, self.n_bits) - 1 

    def _fp(self, sentence : str = None) -> int:
        """
        This function returns the fingerprint of an input string in the range [0, n-1]
        """
        n = self._compute_fp_range()
        return int(hashlib.md5(sentence.encode('utf-8')).hexdigest(), 16) % n

    def build_fingerprints(self, grams : Set[str] = None) -> Tuple[bool, bool, Set[int], float, float]:
        completed = False
        conflict_found = False
        fingerprints = set()
        try:
            if grams:
                for gram in grams:
                    _curr_hash = self._fp(sentence=gram)
                    if not _curr_hash in fingerprints:
                        fingerprints.add(_curr_hash)
                    else:
                        print("\t\tConflict found.")
                        conflict_found = True
                        break
                completed = True
        except Exception as e:
            print(traceback.format_exc())
        finally:
            return completed, conflict_found, fingerprints, self.n_bits/8, asof.asizeof(fingerprints)
    
    def log_fingerprints(self, fingerprints : Set[int] = None) -> bool:
        completed = False
        try:
            if fingerprints:
                with open(f"{os.path.join(self.log_filepath, self.log_filename)}", "w") as fp:
                    for fingerprint in fingerprints:
                        fp.write(str(fingerprint) + "\n")
                completed = True
        except Exception as e:
            print(traceback.format_exc())
        finally:
            return completed
