from flask import Flask, request, session, jsonify
from flask_mysqldb import MySQL
from config import config
import dash_html_components as html
import dash_core_components as dcc
from callbacks import Callback

app = Flask(__name__)

#Conexion a la base de datos
mysql = MySQL(app)

# describes layout of the app
app.title = 'buenos dias'
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page_content')
])
Callback.callback(app)

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
         return jsonify({'mensaje':"No se pudo ver los roles"})
   
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
def pagina_No_Encontrada(err):
    return "<h1>La página a la que intentas acceder no existe</h1>", 404



#inicio del main
if __name__ == '__main__':
    #acceso al diccionario con las credenciales para acceder a la base de datos
    app.config.from_object(config['development'])  
    #para manegar los errores 
    app.register_error_handler(404, pagina_No_Encontrada)
    #run
    app.run(host='0.0.0.0', port=5000)