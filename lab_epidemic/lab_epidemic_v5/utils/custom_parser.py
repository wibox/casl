import argparse

from typing import *

def get_parser() -> Any:
    """
    Initialisation of custom parser. Type python3 main.py --help to get more informations.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--verbosity",
        type=int,
        default=0,
        choices=[0, 1, 2],
        help="Verbosity level for logger."
    )
    return parser.parse_args()