import dash_html_components as html
from . import Button, Datepicker, Dropdown, Input, Modal, NavBar, Table, Textarea, Checklist


# due to the url the getters data change
class CreateComponents:
    def __init__(self, url):
        self.url = url

    def get_checklist(self, app, url, op):
        list_options = []
        if url == 'datosPersonales':
            if op == 0:
                name = 'chklst_residence'
                list_options = ['Domicilio de notificaciones si es distinto del domicilio fiscal']
                default_option = []
            elif op == 1:
                name = 'chklst_disable'
                list_options = ['Discapacidad']
                default_option = []
        elif url == 'datosBancarios':
            name = 'chklst_conditions'
            list_options = ['Acepta las condiciones']
            default_option = []

        chklist = Checklist(name, list_options, default_option).create_checklist()
        container = html.Div([
            chklist
        ],
            className='chklst_container')

        return container

    def get_button(self, app, url, type):
        if type == 'save':
            name = 'btn_save'
            text = 'Enviar'
        elif type == 'export':
            name = 'btn_export'
            text = 'Exportar'
        elif type == 'reload':
            name = 'btn_reload'
            text = 'Recargar'
        elif type == 'clean':
            name = 'btn_clean'
            text = 'Borrar'

        btn = Button(name, text).create_button()
        container = html.Div([
            btn
        ],
            className='btn_container')

        return container

    def get_datepicker(self, app, url):
        name = 'dtpck'

        dtpck = Datepicker(name).create_datepicker()
        container = html.Div([
            dtpck
        ],
            className='dtpck_container')

        return container

    def get_select(self, app, url, op):
        list_options = []
        if url == 'datosEstudios':
            name = 'drpdwn_qualification'
            # list_options = (sacar datos de qalification y pasarlo a una lista)
            default_option = []

        drpdwn = Dropdown(name, list_options, default_option).create_dropdown()
        container = html.Div([
            drpdwn
        ],
            className='drpdwn_container')

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
            className='tbx_container')

        return container

    def get_textarea(self, app, url, id):
        name = 'txta_{}'.format(id)
        textarea = Textarea(name).create_textarea()

        container = html.Div([
            textarea
        ],
            className='txta_container')

        return container

    def get_navbar(self, app, url):
        pass

    def get_header(self, app, url):
        if url == '/login':
            header = html.Div([
                html.Div([
                    html.A([
                        html.Img(id='logo',
                                 src='enlaceatuimagen',
                                 alt='aaahostur hosteleria y turismo')
                    ],
                        href='#'),
                    html.H2('Asociacion española de antiguos alumnos de',
                            'Escuelas de Hosteleria y Turismo'), html.Br()
                ],
                    className='header_up')
            ],
                id='header')

        return header

    def get_footer(self, app, url):
        if url == '/login':
            footer = html.Div([
                html.Div([
                    html.Div([
                        html.H2('Sobre nosotros'),
                        html.P('sssssssssssssssssssiiiiiiiiiiiiiiiiiiiiii'),
                        html.Ul([
                            html.Li([
                                html.A(
                                    html.I(className='fa fa-facebook-square'),
                                    href='#'
                                )
                            ],
                                className='footer_up_col_list_icon'),
                            html.Li([
                                html.A(
                                    html.I(className='fa fa-instagram'),
                                    href='#'
                                )
                            ],
                                className='footer_up_col_list_icon'),
                            html.Li([
                                html.A(
                                    html.I(className='fa fa-twitter'),
                                    href='#'
                                )
                            ],
                                className='footer_up_col_list_icon')
                        ],
                            className='footer_up_col_list')
                    ],
                        className='footer_up_col'),
                    html.Div([
                        html.H2('Links de interes'),
                        html.Ul([
                            html.Li([
                                html.H4(
                                    html.A('Link 1',
                                           href='#')
                                )
                            ],
                                className='footer_up_col_list_link'),
                            html.Li([
                                html.H4(
                                    html.A('Link 2',
                                           href='#')
                                )
                            ],
                                className='footer_up_col_list_link'),
                            html.Li([
                                html.H4(
                                    html.A('Link 3',
                                           href='#')
                                )
                            ],
                                className='footer_up_col_list_link'),
                            html.Li([
                                html.H4(
                                    html.A('Link 4',
                                           href='#')
                                )
                            ],
                                className='footer_up_col_list_link')
                        ],
                            className='footer_up_col_list')
                    ],
                        className='footer_up_col'),
                    html.Div([
                        html.H2('Contactos'),
                        html.Ul([
                            html.Li([
                                html.H4(
                                    html.A('Contacto 1',
                                           href='#')
                                )
                            ],
                                className='footer_up_col_list_link'),
                            html.Li([
                                html.H4(
                                    html.A('Contacto 2',
                                           href='#')
                                )
                            ],
                                className='footer_up_col_list_link'),
                            html.Li([
                                html.H4(
                                    html.A('Contacto 3',
                                           href='#')
                                )
                            ],
                                className='footer_up_col_list_link'),
                            html.Li([
                                html.H4(
                                    html.A('Contacto 4',
                                           href='#')
                                )
                            ],
                                className='footer_up_col_list_link')
                        ],
                            className='footer_up_col_list')
                    ],
                        className='footer_up_col')
                ],
                    id='footer_up'),
                html.Div([
                    html.Ul([
                        html.Li('© 2023',
                                className='footer_down_list_content'),
                        html.Li('-',
                                className='footer_down_list_separator'),
                        html.Li([
                            html.A('AAAHOSTUR',
                                   href='#',
                                   className='footer_down_list_content_link')
                        ],
                            className='footer_down_list_content'),
                        html.Li('-',
                                className='footer_down_list_separator'),
                        html.Li('Todos los derechos reservados',
                                className='footer_down_list_content'),
                        html.Li('-',
                                className='footer_down_list_separator'),
                        html.Li([
                            html.A('Aviso legal',
                                   href='#',
                                   className='footer_down_list_content_link')
                        ],
                            className='footer_down_list_content'),
                        html.Li('-',
                                className='footer_down_list_separator'),
                        html.Li([
                            html.A('Politica de privacidad',
                                   href='#',
                                   className='footer_down_list_content_link')
                        ],
                            className='footer_down_list_content'),
                    ],
                        id='footer_down_list')
                ],
                    id='footer_down')
            ])

        return footer
