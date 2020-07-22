import re
import src.string_utilities as su
import logging
import src.variables as VAR

class header():
    '''Contains the header information found in a .pre file.'''
    def __init__(self, data_input: str):
        #? Stores header data preceding the square bracket entries
        self.meta_data, __discard = su.get_first_array_element(su.split_by_left_square_bracket(data_input))

        #? Processes the square bracket entries to assign as props to the header class.
        square_bracket_entries = re.findall(r'\[(.*?)\]', data_input) #? REGEX to obtain data within '[]' brackets
        for data in square_bracket_entries:
            key_value_pair = su.split_by_equals(data)
            if len(key_value_pair) == 2:
                i = 0
                for entry in key_value_pair:
                    key_value_pair[i] = entry.strip() #? Removes whitespace before assigning a kvp
                    i += 1
                self.__setattr__(key_value_pair[0].lower().replace(' ', '_').replace(',', ''), key_value_pair[1])
            else:
                logging.ERROR('Unable to process a key value pair: {}'.format(str(key_value_pair)))

        self.year_range = self.__get_year_range()

    def __get_year_range(self):
        '''Returns an array of years based on the 'years' property in the header file.'''
        year_range = []
        try:
            years = self.years.split('-')
            if len(years) == 2:
                j = 0
                for year in years:
                    years[j] = int(year.strip())
                    j += 1
                
                for val in range(years[0], years[1] + 1):
                    year_range.append(val)
            else:
                raise Exception('Couldn\'t get two year elements from the following array: {}'.format(str(years)))
        except Exception as e:
            year_range = None
            logging.CRITICAL('Unable to obtain date range! {}'.format(str(e)))
        return year_range

class grid_data():
    #TODO Could add some sanity check here for the precipitation data.
    '''Contains precipitation data as presented in a .pre file.'''
    def __init__(self, x_ref: int, y_ref: int, precipitation_data: list):
        self.x_ref = x_ref
        self.y_ref = y_ref
        self.precipitation_data = precipitation_data
        self.valid_set = False

        if not VAR.HEADER_DATA == None:
            self.validate_precipitation_data(len(VAR.HEADER_DATA.year_range))
        else:
            logging.critical('VAR.HEADER_DATA from variables.py was found to be NoneType when attempting to validate grid data.')
            raise Exception('Header data should be set upstream before attempting to validate grid data!')

    def validate_precipitation_data(self, length: int):
        if len(self.precipitation_data) == length:
            self.valid_set = True
        else:
            logging.warning('Grid-ref: {},{} - precipitation data array (length {}) does not match the year range in the .pre file!'.format(self.x_ref, self.y_ref, len(self.precipitation_data)))

        if any(not len(data) == 12 for data in self.precipitation_data):
            logging.warning('Grid-ref: {},{} contains malformed data!'.format(self.x_ref, self.y_ref))

class sql_data_row():
    '''Object for the subsequent SQL data rows.'''
    def __init__(self):
        self.x_coord = None
        self.y_coord = None
        self.date = None
        self.value = None