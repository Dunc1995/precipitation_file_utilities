#!/usr/bin/python3
import argparse
import src.file_parser as file_parser
import logging

def main(file_path: str):
    data = file_parser.process_pre_file_data(file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Reads a .pre file such that precipitation data can be transformed and uploaded to a SQLite database.')
    parser.add_argument('--input_file_path', '-i', type=str, required=True, help='Input file for processing.')
    parser.add_argument('--log_verbosity', '-v', type=int, default=3, help='Logging verbosity (1 to 5) - level 1 is most verbose, whilst level 5 only logs critical logs.')
    args = parser.parse_args()

    logging.basicConfig(filename='pre_file_utilities.log', filemode='w', level=args.log_verbosity*10)
    main(args.input_file_path)