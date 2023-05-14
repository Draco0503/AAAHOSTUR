import dash_html_components as html
import dash_core_components as dcc

class Dropdown:
    def __init__(self, name, list_option, default_option):
        self.name= name
        self.list_option= list_option
        self.default_option= default_option

    def create_dropdown(self):
        dropdown = dcc.Dropdown(
            options= self.list_option, 
            value= self.default_option,
            placeholder= 'Selecciona una opcion',
            # inline = True,
            id= self.name, 
            className= 'dropdown')
        
        return dropdown