#!/usr/bin/python3
import argparse
import src.prefileparser as file_parser

def main(file_path: str):
    data = file_parser.get_pre_file_data(file_path)
    print(data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Reads a .pre file such that precipitation data can be transformed and uploaded to a SQLite database.')
    parser.add_argument('--input_file_path', '-i', type=str, required=True, help='Input file for processing.')
    args = parser.parse_args()
    main(args.input_file_path)