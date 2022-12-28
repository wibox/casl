from utils.tokenizer import Tokenizer
from utils.fingerprint_handler import FingerprintHandler
from utils.bitstring_array import BitStringArray
from utils.bloom_filter import BloomFilter
from utils.parser import custom_parser
from utils.utils import *

GRAM_SIZE = 6


if __name__ == "__main__":
    args = custom_parser()