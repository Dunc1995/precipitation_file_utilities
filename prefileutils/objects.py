import re
import logging
import sqlite3
import prefileutils.variables as VAR
import prefileutils.stringutils as su

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
                logging.error('Unable to process a key value pair: {}'.format(str(key_value_pair)))

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
            logging.critical('Unable to obtain date range! {}'.format(str(e)))
        return year_range

class grid_data():
    '''Contains precipitation data as presented in a .pre file.'''
    def __init__(self, x_ref: int, y_ref: int, precipitation_data: list):
        self.x_ref = x_ref
        self.y_ref = y_ref
        self.precipitation_data = precipitation_data
        self.is_year_range_valid = False
        self.is_full_annual_set = False
        self.is_complete_dataset = False

        if not VAR.HEADER_DATA == None:
            self.__validate_precipitation_data(len(VAR.HEADER_DATA.year_range))
        else:
            logging.critical('VAR.HEADER_DATA from variables.py was found to be NoneType when attempting to validate grid data.')
            raise Exception('Header data should be set upstream before attempting to validate grid data!')

    def get_monthly_rainfall_data(self):
        '''Collates all monthly rainfall data into the tuple format required for the database.'''
        data_rows = []
        i = 0
        if self.is_complete_dataset:
            for year in self.precipitation_data:
                j = 1
                year_value = VAR.HEADER_DATA.year_range[i]
                for value in year:
                    month = j
                    month_value = "{:02d}".format(month)
                    date = "01/{}/{}".format(month_value, year_value)
                    row = ( self.x_ref, self.y_ref, date, value )
                    data_rows.append(row)
                    j += 1
                i += 1
        
        if not self.is_year_range_valid:
            logging.warning('Ignored Gridref {},{} because of a mismatch between the year range and the given dataset.'.format(self.x_ref, self.y_ref))
        #TODO Make this functionality optional
        if not self.is_full_annual_set:
            logging.warning('Ignored Gridref {},{} because 12 months of data was expected before insertion into the database.'.format(self.x_ref, self.y_ref))
        return data_rows

    def __validate_precipitation_data(self, length: int):
        '''Checks for bad data in the grid and updates its boolean checks accordingly.'''
        if len(self.precipitation_data) == length:
            self.is_year_range_valid = True
        else:
            logging.warning('Grid-ref: {},{} - precipitation data array (length {}) does not match the year range in the .pre file!'.format(self.x_ref, self.y_ref, len(self.precipitation_data)))

        if any(not len(data) == 12 for data in self.precipitation_data):
            logging.warning('Grid-ref: {},{} contains malformed data!'.format(self.x_ref, self.y_ref))
        else:
            self.is_full_annual_set = True
        
        if self.is_full_annual_set and self.is_year_range_valid:
            self.is_complete_dataset = True

class sql_db():
    '''Barebones sqlite3 wrapper.'''
    #TODO Would be straightforward to alter this to work with a SQL server.
    def __init__(self, database_name: str):
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()

    def create_precipitation_data_table(self):
        '''Creates the Precipitation_Data table if it does not already exist.'''
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Precipitation_Data ( Xref integer, Yref integer, Date text, Value integer )''')
        self.connection.commit()

    def insert_data_array(self, data_array: list):
        '''Designed to bulk upload on a per grid basis.'''
        #TODO Optimise this function
        self.cursor.execute("BEGIN TRANSACTION;")
        self.cursor.executemany('INSERT INTO Precipitation_Data VALUES (?,?,?,?)', data_array)
        self.cursor.execute("COMMIT;")