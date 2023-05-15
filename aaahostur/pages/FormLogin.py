import dash_core_components as dcc
import dash_html_components as html
from aaahostur.components.CreateComponents import CreateComponents


# returns a html container
def create_layout_login(app=None, url=None):
    cc = CreateComponents(url)
    # page
    page = html.Div([
        html.Header([
            cc.get_header(app, url),
            html.Nav([
                cc.get_navbar(app, url)
            ])
        ],
            id='header',
            className='header'),
        html.Main([

        ],
            id='main',
            className='main'),
        html.Footer([
            cc.get_footer(app, url)
        ],
            id='footer',
            className='footer')
    ],
        id='page',
        className='page')

    return page
# TEXBOX: Email
# TEXBOX_PASSWORD: PWD
