import dash_core_components as dcc
import dash_html_components as html
from components import CreateComponents

# returns a html container
def create_layout_form_0(app= None, url= None):
    # page
    page = html.Div([
        html.Header([
            CreateComponents().get_header(app, url)
        ], 
        id= 'header', 
        className= 'header'),
        html.Main([
            
        ]),
        html.Footer([
            CreateComponents().get_footer(app, url)
        ], 
        id= 'footer', 
        className= 'footer')
    ],
    id='page',
    className='page')

    return page