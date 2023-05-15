from flask import Flask, request, session, json, render_template, Response
from models import db
from models import Language, Job_Category, Qualification, Role, User, Member, Member_Account, Member_Language,\
    Academic_Profile, Professional_Profile, Section, Company, Company_Account, Offer, Member_Offer, Job_Demand, \
    Job_Demand_Language, Job_Demand_Qualification, Job_Demand_Category, Review
from config import config


app = Flask(__name__)
# describes layout of the app


# metodo de prueba de conexion
@app.route('/prueba')
def index():
    try:
        return '<h1>Prueba</h1>'
    except Exception as ex:
        return "Error"


@app.route('/api_v0/role-list', methods=['GET'])
def role_list():
    msg = {"roles": [role.to_json() for role in Role.Role.query.all()]}
    return Response(json.dumps(
        msg,
    ), status=200)


# FUNCIONES PARA LOS ERRORES MAS COMUNES

# Error 404-not found
def not_Found(err):
    return "<h1>La página a la que intentas acceder no existe</h1>", 404


# Error 403-forbidden
def inadequate_Permits(err):
    return "<h1>No tienes los permisos necesarios para acceder a este contenido</h1>", 403


# Error 429-Too many request
def too_Many_Request(err):
    return "<h1>Has enviado demasiadas solicitudes en poco tiempo, Espere un poco</h1>", 429


# Error 500-Internal server error
def internal_Server_Error(err):
    return "<h1>En mantenimiento</h1>", 500


# Error 504 Gateway Timeout
def bad_Request(err):
    return "<h1>Timeout</h1>", 504


# inicio del main
if __name__ == '__main__':
    # acceso al diccionario con las credenciales para acceder a la base de datos
    app.config.from_object(config['development'])  
    # Conexion con la base de datos
    db.init_app(app)
    with app.app_context():
        db.create_all()
    # para manegar los errores
    app.register_error_handler(404, not_Found)
    app.register_error_handler(403, inadequate_Permits)
    app.register_error_handler(429, too_Many_Request)
    app.register_error_handler(500, internal_Server_Error)
    app.register_error_handler(504, bad_Request)
    # run
    app.run(host='0.0.0.0', port=5000)