# -*- coding: utf-8 -*-
import pandas as pd
from callbacks import CallbackForm0
from utils import URL
from pages import Form0
from dash.dependencies import Input, Output, State

def callback(app):

    CallbackForm0.callback_form_0(app)

    @app.callback(Output('page_content', 'children', allow_duplicate=True),
                  Input('url', 'pathname'),
                  prevent_initial_call=True)
    def display_page(pathname):
        if pathname == URL + 'form0':
            return Form0.create_layout_form_0(app, pathname)
        else:
            return Form0.create_layout_form_0(app, pathname)