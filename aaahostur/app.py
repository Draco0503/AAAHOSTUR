from dotenv import load_dotenv
from flask import Flask, request, session
from flask_mysqldb import MySQL
from config import config

app = Flask(__name__)

#Conexion a la base de datos
mysql = MySQL(app)

#metodo de prueba de conexion
@app.route('/prueba')
def index():
    try:
        return '<h1>Prueba JIJIJAJeje</h1>'
    except Exception as ex:
        return "Error"

#FUNCIONES PARA LOS ERRORES MAS COMUNES

#Error 404-not found
def pagina_No_Encontrada(err):
    return "<h1>La página a la que intentas acceder no existe</h1>"



#inicio del main
if __name__ == '__main__':
#acceso al diccionario con las credenciales para acceder a la base de datos
 app.config.from_object(config['development'])  
#para manegar los errores 
 app.register_error_handler(404, pagina_No_Encontrada)
 #run
 app.run()