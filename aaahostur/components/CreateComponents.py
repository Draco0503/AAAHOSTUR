import dash_html_components as html
from components import Button, Datepicker, Dropdown, Input, Modal, Navbar, Table, Title

# due to the url the getters data change
class CreateComponents:
    def __init__(self, url):
        self.url = url

    def get_header(self, app, url):
        if (url == self.url) or (url == self.url + 'form0'):
            # pasar info de header de form0
            name = 'headerForm0'
            header = Title.Title(name).create_title()
        else:
            # pasar info de header de formN
            name = 'headerFormN'
            header = Title.Title(name).create_title()

        return header
    
    def get_select(self, app, url):
        list_dropdown = []
        if (url == self.url) or (url == self.url + 'form0'):
            # pasar info de header de form0
            name = 'headerForm0'
            selects = Title.Title(name).create_title()
        else:
            # pasar info de header de formN
            name = 'headerFormN'
            selects = Title.Title(name).create_title()

        return selects
    
    def get_table(self, app, url):
        list_table = []
        if (url == self.url) or (url == self.url + 'form0'):
            # pasar info de header de form0
            name = 'headerForm0'
            tables = Title.Title(name).create_title()
        else:
            # pasar info de header de formN
            name = 'headerFormN'
            tables = Title.Title(name).create_title()

        return tables
    
    def get_button(self, app, url):
        list_button = []
        if (url == self.url) or (url == self.url + 'form0'):
            # pasar info de header de form0
            name = 'headerForm0'
            buttons = Title.Title(name).create_title()
        else:
            # pasar info de header de formN
            name = 'headerFormN'
            buttons = Title.Title(name).create_title()

        return buttons
    
    def get_modal(self, app, url):
        if (url == self.url) or (url == self.url + 'form0'):
            # pasar info de header de form0
            name = 'headerForm0'
            modal = Title.Title(name).create_title()
        else:
            # pasar info de header de formN
            name = 'headerFormN'
            modal = Title.Title(name).create_title()

        return modal
    
    def get_menu(self, app, url):
        if (url == self.url) or (url == self.url + 'form0'):
            # pasar info de header de form0
            name = 'headerForm0'
            menu = Title.Title(name).create_title()
        else:
            # pasar info de header de formN
            name = 'headerFormN'
            menu = Title.Title(name).create_title()

        return menu
    
    def ge_input(self, app, url):
        list_input = []
        if (url == self.url) or (url == self.url + 'form0'):
            # pasar info de header de form0
            name = 'headerForm0'
            input = Title.Title(name).create_title()
        else:
            # pasar info de header de formN
            name = 'headerFormN'
            input = Title.Title(name).create_title()

        return input
    
    def get_datepicker(self, app, url):
        if (url == self.url) or (url == self.url + 'form0'):
            # pasar info de header de form0
            name = 'headerForm0'
            datepicker = Title.Title(name).create_title()
        else:
            # pasar info de header de formN
            name = 'headerFormN'
            datepicker = Title.Title(name).create_title()

        return datepicker