from os.path import exists
import json
import logging
from src.objects import header, grid_data
import src.stringutils as su
from src.stringutils import get_first_array_element, get_integer_array
import src.variables as VAR

def process_file(file_path: str):
    '''Attempts to parse a .pre file header and its grid reference blocks. Returns false if the process fails.'''
    success = False
    try:
        #? Read file contents
        file_contents = __get_file_contents(file_path)
        
        #? Separate file header from the grid data
        file_header_string, grid_string_array = get_first_array_element(su.split_by_grid_reference(file_contents))
        VAR.HEADER_DATA = header(file_header_string)

        for grid_string in grid_string_array:
            #? Separate coordinate string from precipitation data
            coordinate_string, precipitation_string_array = get_first_array_element(su.split_by_newline(grid_string))

            xy_coords = get_integer_array(su.split_by_comma(coordinate_string)) #* XY reference coordinates

            annual_precipitation_array = [] #! Should expect arrays of length 12 appended to this array
            for pre_string in precipitation_string_array:
                raw_string_array = su.split_default(pre_string)
                
                if len(raw_string_array) > 0:
                    precipitation_integer_array = get_integer_array(raw_string_array) #* Integer array for 1 year of precipitation data
                    annual_precipitation_array.append(precipitation_integer_array)
                else:
                    logging.debug('Array of length {} was ignored when processing precipitation data.'.format(len(raw_string_array)))

            VAR.GRID_DATA_ARRAY.append(grid_data(xy_coords[0], xy_coords[1], annual_precipitation_array))
        
        success = True
    except Exception as e:
        logging.critical('Failed to process "{}": {}'.format(file_path, str(e)))
    return success

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