import re

class header():
    '''Contains the header information found in a .pre file.'''
    def __init__(self, data_input: str):
        output = re.findall(r'\[(.*?)\]', data_input)
        print(str(output))

class grid_data():
    #TODO Could add some sanity check here for the precipitation data.
    '''Contains precipitation data as presented in a .pre file.'''
    def __init__(self, x_ref: int, y_ref: int, precipitation_data: list):
        self.x_ref = x_ref
        self.y_ref = y_ref
        self.precipitation_data = precipitation_data
        

class sql_data_row():
    '''Object for the subsequent SQL data rows.'''
    def __init__(self):
        self.x_coord = None
        self.y_coord = None
        self.date = None
        self.value = None