import dash_html_components as html

class Title:
    def __init__(self, name):
        self.name = name

    def create_title(self):
        id_title = self.name
        title = html.Div([
            html.P('Tu madre')
        ])
        return title
    