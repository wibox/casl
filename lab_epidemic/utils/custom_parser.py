import argparse

from typing import *

def get_parser() -> Any:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--verbosity",
        type=int,
        default=1,
        help="Verbosity level for logger."
    )
    return parser.parse_args()