import dash_html_components as html
import dash_core_components as dcc

class Button:
    def __init__(self, name, text):
        self.name= name
        self.text= text

    def create_button(self):
        button = html.Button(
            self.text,
            id= self.name, 
            className= 'button')
        
        return button