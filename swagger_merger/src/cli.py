import argparse
import swagger_merger


def main():
    parser = argparse.ArgumentParser(prog='merger',
                                     description='swagger merger package.')
    parser.add_argument('-f', dest="input_file", help='Name of the input file')
    parser.add_argument('-o', dest="output_file", help='Name of the output file')
    args = parser.parse_args()
    swagger_merger.merge(args.input_file, ".", args.output_file, ".")
