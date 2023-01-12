import argparse

def custom_parser():
    """
    Custom parser definition.
    Current implementation only allows for the input filename to be parsed.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--filename",
        type=str,
        default="divina_commedia.txt",
        help="Input filesname from which all simulation is carried out."
    )
    return parser.parse_args()