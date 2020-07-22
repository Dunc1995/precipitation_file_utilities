NEWLINE = '\n'
GRID_DELIMITER = 'Grid-ref='
COMMA = ','
EQUALS = '='
LEFT_SQUARE_BRACKET = '['

#region public split functions
def split_by_newline(input: str):
    return __split(input, NEWLINE)

def split_by_grid_reference(input: str):
    return __split(input, GRID_DELIMITER)

def split_by_equals(input: str):
    return __split(input, EQUALS)

def split_by_comma(input: str):
    return __split(input, COMMA)

def split_by_left_square_bracket(input: str):
    return __split(input, LEFT_SQUARE_BRACKET)

def split_default(input: str):
    return __split(input)
#endregion

def __split(input: str, delimiter: str = None):
    '''Wrapper for the str().split() method.'''
    return input.split(delimiter)

def get_first_array_element(data_array: list):
    '''Separates the first element from the rest of the array.'''
    first_element = data_array.pop(0)
    return first_element, data_array

def get_integer_array(data_array: list):
    '''Attempts to cast the input array as an array of integers.'''
    integer_array = []
    try:
        for entry in data_array:
            integer_array.append(int(entry.strip()))
        
        if len(integer_array) == 0:
            raise Exception('Cannot cast an empty array to an integer array!')
    except Exception as e:
        print('Error trying to obtain integer array: {}'.format(str(e)))
        integer_array = None
    return integer_array