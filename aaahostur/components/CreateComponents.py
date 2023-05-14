import dash_html_components as html
from components import Button, Datepicker, Dropdown, Input, Modal, Navbar, Table, Title, Textarea, Checklist

# due to the url the getters data change
class CreateComponents:
    def __init__(self, url):
        self.url = url

    def get_checklist(self, app, url, op):
        list_options = []
        if url == 'datosPersonales':
            if op == 0:
                name= 'chklst_residence'
                list_options= ['Domicilio de notificaciones si es distinto del domicilio fiscal']
                default_option = []
            elif op == 1:
                name= 'chklst_disable'
                list_options= ['Discapacidad']
                default_option = []               
        elif url == 'datosBancarios':
            name= 'chklst_conditions'
            list_options= ['Acepta las condiciones']
            default_option = []  

        chklist= Checklist(name, list_options, default_option).create_checklist()
        container = html.Div([
            chklist
        ], 
        className= 'chklst_container')

        return container

    def get_button(self, app, url, type):
        if type == 'save':
            name= 'btn_save'
            text= 'Enviar'
        elif type == 'export':
            name= 'btn_export'
            text= 'Exportar'
        elif type == 'reload':
            name= 'btn_reload'
            text= 'Recargar'
        elif type == 'clean':
            name= 'btn_clean'
            text= 'Borrar'

        btn = Button(name, text).create_button()
        container = html.Div([
            btn
        ], 
        className= 'btn_container')

        return container
    
    def get_datepicker(self, app, url):
        name = 'dtpck'

        dtpck = Datepicker(name).create_datepicker()
        container = html.Div([
            dtpck
        ], 
        className= 'dtpck_container')

        return container
    
    def get_select(self, app, url, op):
        list_options = []
        if url == 'datosEstudios':
            name= 'drpdwn_qualification'
            # list_options = (sacar datos de qalification y pasarlo a una lista)
            default_option= []

        drpdwn = Dropdown(name, list_options, default_option).create_dropdown()
        container = html.Div([
            drpdwn
        ], 
        className= 'drpdwn_container')

        return container
    
    def get_input(self, app, url, type, id):
        if type == 'number':
            name = 'tbx_number_{}'.format(id)
            input = Input(name, type).create_input_number()
        else:
            name = 'tbx_text_{}'.format(id)
            input = Input(name, type).create_input_text()

        container = html.Div([
            input
        ], 
        className= 'tbx_container')

        return container
    
    def get_textarea(self, app, url, id):
        name = 'txta_{}'.format(id)
        textarea = Textarea(name).create_textarea()

        container = html.Div([
            textarea
        ], 
        className= 'txta_container')

        return container
    
    def get_header(self, app, url):
        if True:
            # make the header for each tab
            header = None

        return header
