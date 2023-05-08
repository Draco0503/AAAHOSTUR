from flask import Flask, request, session, jsonify
from flask_mysqldb import MySQL
from config import config

app = Flask(__name__)

#Conexion a la base de datos
mysql = MySQL(app)

#metodo de prueba de conexion
@app.route('/prueba')
def index():
    try:
        return '<h1>Prueba</h1>'
    except Exception as ex:
        return "Error"
    
@app.route('/listaUsuarios', methods=['GET'])
def usuarios():
   try:
        cursor = mysql.connection.cursor()
        sql = "SELECT UserName, UserPass FROM users"
        cursor.execute(sql)
        #almacena el resultado de la query y lo "traduce" a python
        datos=cursor.fetchall()
        print(datos)
        listaUsuarios=[]
        #for para recorrer todos los datos sacados y almacenarlos en un objeto 
        for fila in datos:
            usuario = {'UserName':fila[0], 'UserPass':fila[1]}
            #se agrega el usuario a la lista de usuarios
            listaUsuarios.append(usuario)
        return jsonify({'usuarios':listaUsuarios, 'mensaje':"Esta es la lista de usuarios"})
   except Exception as ex:
         return jsonify({'mensaje':"No funciono el mostrar la lista de usuarios...."})
   
@app.route('/registrarUsuario', methods=['POST'])
def registrarUsuarios():
   try:
        cursor = mysql.connection.cursor()
        sql = f"INSERT INTO users (UserName, UserPass) VALUES('{0}','{1}','{2}')".format(request.json['UserName'], request.json['UserPass'])
        cursor.execute(sql)
        mysql.connection.commit()
        return jsonify({'mensaje':"Usuario Registrado"})
   except Exception as ex:
         return jsonify({'mensaje':"Error al registrar...."})


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