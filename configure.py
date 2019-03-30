import argparse
import sys


def parse_args():
    """
    Parse input arguments
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("--input_path", default="./example_data/Kolodziejczyk.csv",
                        type=str, help="path of input data")
    parser.add_argument("--lower_bound", default=96,
                        type=int, help="lower bound of estimated low-quality \
                        cell number")
    parser.add_argument("--upper_bound", default=192,
                        type=int, help="upper bound of estimated low-quality \
                        cell number")
    parser.add_argument("--labeled", default=True,
                        help="whether the data has \
                        quality labels. If true, evaluation information will be \
                        printed.", type=lambda x: (str(x).lower() == 'true'))
    parser.add_argument("--output_path", default="./result.csv",
                        type=str, help="path of output data")

    if len(sys.argv) == 0:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    return args

FLAGS = parse_args()
