import dash_html_components as html
import dash_core_components as dcc

class Input:
    # valid types ["text", "number", "password", "email", "search", "tel", "url", "range", "hidden"]
    def __init__(self, name, type):
        self.name= name
        self.type= type

    def create_input_text(self):
        input = dcc.Input(
            type= self.type, 
            placeholder= 'Insert text',
            id= self.name, 
            className= 'input')
        
        return input
    
    def create_input_number(self):
        input = dcc.Input(
            type= self.type,
            placeholder= 'Insert number',
            # min= 0, # max value selectable
            # max= 100, # min value selectable
            # step= 1, # step by step
            id= self.name,
            className= 'input')

        return input
    