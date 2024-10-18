import argparse
import sys


def parse_args():
    """
    Parse input arguments
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("--input_path", default="./example_data/Kolodziejczyk.csv",
                        type=str, help="path of input data")
    parser.add_argument("--lower_bound", default=None,
                        type=int, help="lower bound of estimated low-quality \
                        cell number")
    parser.add_argument("--upper_bound", default=None,
                        type=int, help="upper bound of estimated low-quality \
                        cell number")
    parser.add_argument("--labeled", default=True,
                        help="whether the data has \
                        quality labels. If true, evaluation information will be \
                        printed.", type=lambda x: (str(x).lower() == 'true'))
    parser.add_argument("--output_path", default=None,
                        type=str, help="path of output data")
    parser.add_argument("--organism", required=True,
                        type=str, choices=['human', 'mouse'], help="species of the organism (human or mouse)")
    parser.add_argument("--normalize", default=True,
                        type=lambda x: (str(x).lower() == 'true'), help="whether to normalize the data (default: True)")


    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    return args

FLAGS = parse_args()
