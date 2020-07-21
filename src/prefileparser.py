from os.path import exists

def get_pre_file_data(file_path: str):
    '''Attempts to read the input file path and return its contents as a string.'''
    output_data = None

    if exists(file_path):
        if file_path.endswith('.pre'):
            with open(file_path, 'r') as file:
                output_data = file.read()
        else:
            raise Exception('Input file format not supported! This script is only able to read .pre files.')
    else:
        raise Exception('Path \"{}\" does not exist!'.format(file_path))

    return output_data