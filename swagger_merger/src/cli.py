import argparse
import swagger_merger


def main():
    parser = argparse.ArgumentParser(prog='merger',
                                     description='swagger merger package.')
    parser.add_argument('-f')
    args = parser.parse_args()
    swagger_merger.merge(args.f, ".", "swagger.yml", ".")
