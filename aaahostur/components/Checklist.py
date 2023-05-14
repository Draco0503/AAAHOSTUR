import dash_html_components as html
import dash_core_components as dcc

class Checklist:
    def __init__(self, name, list_option, default_option):
        self.name = name
        self.list_option = list_option
        self.default_option = default_option

    def create_checklist(self):
        checklist = dcc.Checklist(
            options= self.list_option, 
            value= self.default_option,
            # inline = True,
            id= self.name, 
            className= 'chklst')
        
        return checklist