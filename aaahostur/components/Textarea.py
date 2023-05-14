import dash_html_components as html
import dash_core_components as dcc

class Textarea:
    def __init__(self, name):
        self.name = name

    def create_textarea(self):
        textarea = dcc.Textarea(
            placeholder= 'Insert long text',
            # maxLength= '100' # max characters
            id= self.name,
            className= 'txta')

        return textarea