from os.path import exists

# class grid():
#     def __init__(self, ):
#         self.x_ref
#         self.y_ref


def process_pre_file_data(file_path: str):
    #? Read file contents
    data_string = __get_pre_file_data_string(file_path)
    
    #? Separate file header from the grid data
    file_header_string, grid_string_array = __get_first_element_and_subsequent_array(data_string, 'Grid-ref=')
    
    for grid_string in grid_string_array:
        #? Separate coordinate string from precipitation data
        coordinate_string, precipitation_string_array = __get_first_element_and_subsequent_array(grid_string, '\n')

        xy_integer_coordinates = __get_integer_data_array(coordinate_string, ',') #* XY reference coordinates
        for pre_string in precipitation_string_array:
            precipitation_integer_array = __get_integer_data_array(pre_string, None) #* Integer array for 1 year of precipitation data

def __get_pre_file_data_string(file_path: str):
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

def __get_first_element_and_subsequent_array(data: str, delimiter: str):
    '''Splits the input string according to the input delimiter, then separates the first element from the rest of the array.'''
    data_array = data.split(delimiter)
    first_element = data_array.pop(0)
    return first_element, data_array

def __get_integer_data_array(data: str, delimiter:str):
    '''Splits the input data string and outputs its elements as an array of integers.'''
    integer_array = []
    try:
        string_array = data.split(delimiter)
        for entry in string_array:
            integer_array.append(int(entry.strip()))
    except Exception as e:
        print('Error trying obtain integer array: {}'.format(str(e)))
        integer_array = None
    return integer_array