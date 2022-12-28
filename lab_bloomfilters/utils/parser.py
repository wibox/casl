import argparse

def custom_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--filename",
        type=str,
        default="divina_commedia.txt",
        help="Input filesname from which all simulation is carried out."
    )
    return parser.parse_args()