#!/usr/bin/python3
import argparse
import logging
import json
import src.parser as file_parser
import src.variables as VAR
from src.objects import sql_db

def main(file_path: str):
    data_is_parsed = file_parser.process_file(file_path)
    if data_is_parsed == True:
        db = sql_db('./data/precipitationdata.db')
        db.create_precipitation_data_table()
        for grid in VAR.GRID_DATA_ARRAY:
            logging.info('Uploading data for Gridref {},{}'.format(grid.x_ref, grid.y_ref))
            db.insert_data_array(grid.get_monthly_rainfall_data())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Reads a .pre file such that precipitation data can be transformed and uploaded to a SQLite database.')
    parser.add_argument('--input_file_path', '-i', type=str, required=True, help='Input file for processing.')
    parser.add_argument('--log_verbosity', '-v', type=int, default=2, help='Logging verbosity (1 to 5) - level 1 is most verbose, level 5 logs critical entries only.')
    args = parser.parse_args()

    logging.basicConfig(filename='./data/predatauploader.log', filemode='w', level=args.log_verbosity*10)
    main(args.input_file_path)