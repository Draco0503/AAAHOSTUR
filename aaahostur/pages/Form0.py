import dash_core_components as dcc
import dash_html_components as html
from utils import Header, Select, Table, Button, Modal, Menu, Input, DatePicker

# returns a html container
def create_layout_form_0(app= None, url= None):
    # page
    page = html.Div([
        html.Div([
            Header(app, url)
        ],
        id='header_container0',
        className='header_container',
        style={}),
        # sub page
        html.Div([
            # menu
            html.Div([
                Menu(app, url)
            ],
            id='menu_container0',
            className='menu_container',
            style={}),
            # filter
            html.Div([
                Select(app, url)
            ],
            id='select_container0',
            className='select_container',
            style={}),
            # button
            html.Div([
                Button(app, url)
            ],
            id='button_container0',
            className='button_container',
            style={})
        ],
        id='sub_page0',
        className='sub_page',
        style={})
    ],
    id='page0',
    className='page',
    style={})

    return page