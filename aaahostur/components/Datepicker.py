import dash_html_components as html
import dash_core_components as dcc
from datetime import date

class Datepicker:
    def __init__(self, name):
        self.name = name

    def create_datepicker(self):
        datepicker = dcc.DatePickerSingle(
            # min_date_allowed= date(1999, 1, 1), # max date allowed
            # max_date_allowed= date(2023, 12, 1), # min date allowed
            # clearable= True, # an 'x' button appears to erase selected date
            # with_portal= True, # displays de datepicker in a small screen
            # date= date(1999, 1, 1), # value
            placeholder= 'Escoge una fecha',
            id= self.name,
            className= 'datepicker')
        
        return datepicker
        