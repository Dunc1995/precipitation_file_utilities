from os.path import exists
from src.data_objects import header, grid_data
import src.string_utilities as su
from src.string_utilities import get_first_array_element, get_integer_array
import json
import logging

def process_pre_file_data(file_path: str):
    grid_data_array = []

    #? Read file contents
    file_contents = __get_file_contents(file_path)
    
    #? Separate file header from the grid data
    file_header_string, grid_string_array = get_first_array_element(su.split_by_grid_reference(file_contents))
    test = header(file_header_string)


    for grid_string in grid_string_array:
        #? Separate coordinate string from precipitation data
        coordinate_string, precipitation_string_array = get_first_array_element(su.split_by_newline(grid_string))

        xy_coords = get_integer_array(su.split_by_comma(coordinate_string)) #* XY reference coordinates

        annual_precipitation_array = [] #! Should expect arrays of length 12 appended to this array
        for pre_string in precipitation_string_array:
            raw_string_array = su.split_default(pre_string)
            
            if len(raw_string_array) == 12: #TODO Add sanity checks to the grid_data class instead of here.
                precipitation_integer_array = get_integer_array(raw_string_array) #* Integer array for 1 year of precipitation data
                annual_precipitation_array.append(precipitation_integer_array)
            else:
                logging.debug('Array of length {} was ignored when processing precipitation data.'.format(len(raw_string_array)))

        grid_data_array.append(grid_data(xy_coords[0], xy_coords[1], annual_precipitation_array))
    
    # for grid in grid_data_array:
    #     print(json.dumps(grid.__dict__, indent=4))

def __get_file_contents(file_path: str):
    '''Attempts to read the input file path and return its contents as a string.'''
    file_contents = None

    if exists(file_path):
        if file_path.endswith('.pre'):
            with open(file_path, 'r') as file:
                file_contents = file.read()
        else:
            raise Exception('Input file format not supported! This script is only able to read .pre files.')
    else:
        raise Exception('Path \"{}\" does not exist!'.format(file_path))

    return file_contents