import dash_html_components as html
import pandas as pd
from components import CreateComponents

URL =''

def header(app= None, url= None):
    return html.Div([
        CreateComponents(URL).get_header(app, url)
    ])

def select(app= None, url= None):
    return html.Div([
        CreateComponents(URL).get_select(app, url)
    ])

def table(app= None, url= None):
    return html.Div([
        CreateComponents(URL).get_table(app, url)
    ])

def button(app= None, url= None):
    return html.Div([
        CreateComponents(URL).get_button(app, url)
    ])

def modal(app= None, url= None):
    return html.Div([
        CreateComponents(URL).get_modal(app, url)
    ])

def menu(app= None, url= None):
    return html.Div([
        CreateComponents(URL).get_menu(app, url)
    ])

def input(app= None, url= None):
    return html.Div([
        CreateComponents(URL).ge_input(app, url)
    ])

def datepicker(app= None, url= None):
    return html.Div([
        CreateComponents(URL).get_datepicker(app, url)
    ])