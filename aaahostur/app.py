from flask import Flask, request, session, jsonify
from flask_mysqldb import MySQL
from config import config
#import dash_html_components as html
#import dash_core_components as dcc
#from callbacks import Callback

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
    
@app.route('/listaRoles', methods=['GET'])
def roles():
    try:
        cursor = mysql.connection.cursor()
        sql = "SELECT ID_ROLE, Name, Description FROM Role"
        cursor.execute(sql)
        #almacena el resultado de la query y lo "traduce" a python
        datos=cursor.fetchall()
        listaRoles=[]
        #for para recorrer todos los datos sacados y almacenarlos en un objeto 
        for fila in datos:
            role = {'ID_ROLE':fila[0], 'Name':fila[1], 'Description':fila[2]}
            #se agrega el usuario a la lista de usuarios
            listaRoles.append(role)
        return jsonify({'roles':listaRoles, 'mensaje':"Esta es la lista de Roles"})
    except Exception as ex:
         return jsonify({'mensaje':"No se pudo ver los roles"})
    
@app.route('/verUsuarios', methods=['GET'])
def usuarios():
    try:
        cursor = mysql.connection.cursor()
        sql = "SELECT Passwd, Email, id_Role FROM User"
        cursor.execute(sql)
        #almacena el resultado de la query y lo "traduce" a python
        datos=cursor.fetchall()
        listaUser=[]
        #for para recorrer todos los datos sacados y almacenarlos en un objeto 
        for fila in datos:
            user = {'Passwd':fila[0], 'Email':fila[1], 'id_Role':fila[2]}
            #se agrega el usuario a la lista de usuarios
            listaUser.append(user)
        return jsonify({'Usuarios':listaUser, 'mensaje':"Esta es la lista de usuarios"})
    except Exception as ex:
         return jsonify({'mensaje':"No se pudo ver los usuarios"})
   
@app.route('/registrarSuperAdmin', methods=['POST'])
def registrarSuperAdmin():
   try:
        print(request.json)
        cursor = mysql.connection.cursor()
        sql = """INSERT INTO User (ID_USER, Passwd, Email, id_Role)
        VALUES({0}, '{1}', '{2}', {3})""".format(request.json['ID_USER'],
        request.json['Passwd'], request.json['Email'], request.json['id_Role'])
        cursor.execute(sql)
        mysql.connection.commit()
        return jsonify({'mensaje':"Usuario Registrado"})
   except Exception as ex:
         return jsonify({'mensaje':"Error al registrar...."})
   
@app.route('/registrarAdmin', methods=['POST'])
def registrarAdmin():
   try:
        print(request.json)
        cursor = mysql.connection.cursor()
        sql = """INSERT INTO User (Passwd, Email, id_Role)
        VALUES('{0}', '{1}', {2})""".format(request.json['Passwd'], 
        request.json['Email'], request.json['id_Role'])
        cursor.execute(sql)
        mysql.connection.commit()
        return jsonify({'mensaje':"Usuario Registrado"})
   except Exception as ex:
         return jsonify({'mensaje':"Error al registrar...."})
   
@app.route('/registrarUsuario', methods=['POST'])
def registrarUsuario():
   try:
        print(request.json)
        cursor = mysql.connection.cursor()
        sql = """INSERT INTO User (Passwd, Email, id_Role)
        VALUES('{0}', '{1}', {2})""".format(request.json['Passwd'], 
        request.json['Email'], request.json['id_Role'])
        typeMember = request.json['id_Role']
        prueba = cursor.execute(sql)
        print(prueba)
        sql2 = "SELECT max(ID_USER) FROM User"
        id = cursor.execute(sql2)    
        match typeMember:
            case 104:
                print("Insertar Miembro")
                print(id)
                sql3 = "INSERT INTO Member (ID_MEMBER, Name, Surname) VALUES("+ id + ", '{3}', '{4}')".format(request.json['Name'], request.json['Surname'])
                cursor.execute(sql3)
            case 105:
                print("Insertar Compañia")
            case _:
                print("Caso Default")

        mysql.connection.commit()
        return jsonify({'mensaje':"Usuario Registrado"})
   except Exception as ex:
         mysql.connection.rollback()
         return jsonify({'mensaje':"Error al registrar...."})
        

#FUNCIONES PARA LOS ERRORES MAS COMUNES

#Error 404-not found
def not_Found(err):
    return "<h1>La página a la que intentas acceder no existe</h1>", 404


#Error 403-forbidden
def inadequate_Permits(err):
    return "<h1>No tienes los permisos necesarios para acceder a este contenido</h1>", 403


#Error 429-Too many request
def too_Many_Request(err):
    return "<h1>Has enviado demasiadas solicitudes en poco tiempo, Espere un poco</h1>", 429


#Error 500-Internal server error 
def internal_Server_Error(err):
    return "<h1>En mantenimiento</h1>", 500

#Error 504 Gateway Timeout
def bad_Request(err):
    return "<h1>ns que poner aqui jijijajaja</h1>", 504



#inicio del main
if __name__ == '__main__':
    #acceso al diccionario con las credenciales para acceder a la base de datos
    app.config.from_object(config['development'])  
    #para manegar los errores 
    app.register_error_handler(404, not_Found)
    app.register_error_handler(403, inadequate_Permits)
    app.register_error_handler(429, too_Many_Request)
    app.register_error_handler(500, internal_Server_Error)
    app.register_error_handler(504, bad_Request)
    #run
    app.run(host='0.0.0.0', port=5000)